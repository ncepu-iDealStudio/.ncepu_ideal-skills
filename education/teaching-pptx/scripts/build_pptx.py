"""Build an editable, text-first 16:9 teaching deck from a UTF-8 JSON file."""

import argparse
import io
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple


METADATA_START = '[[TEACHING_PPTX_METADATA]]'
METADATA_END = '[[/TEACHING_PPTX_METADATA]]'
METADATA_VERSION = 1


# layout: minimum points, maximum points, maximum width units per point
LAYOUTS = {
    'bullets': (1, 4, 64),
    'focus': (1, 1, 60),
    'compare': (2, 2, 56),
    'steps': (2, 4, 60),
    'practice': (1, 3, 60),
}


@dataclass(frozen=True)
class SlideSpec:
    title: str
    label: str
    points: Tuple[str, ...]
    notes: str
    layout: str
    activity: Optional[str] = None


@dataclass(frozen=True)
class DeckSpec:
    title: str
    subtitle: str
    cover_notes: str
    slides: Tuple[SlideSpec, ...]
    audience: Optional[str] = None
    learning_objectives: Optional[Tuple[str, ...]] = None
    duration_minutes: Optional[int] = None

    @property
    def has_teaching_metadata(self):
        return self.audience is not None


def units(text):
    return sum(2 if unicodedata.east_asian_width(c) in 'WFA' else 1 for c in text)


def text_field(item, key, prefix, *, limit=None, multiline=False):
    value = item.get(key)
    label = f'{prefix}.{key}'
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be nonempty text')
    value = value.strip().replace('\r\n', '\n')
    if (not multiline and (len(value.splitlines()) != 1 or '\n' in value)
            or re.search(r'[\x00-\x09\x0b-\x1f\x7f\u2028\u2029]', value)):
        raise ValueError(f'{label} contains an unsupported line break or control character')
    if limit is not None and units(value) > limit:
        raise ValueError(f'{label} exceeds {limit} width units; shorten it')
    return value


def parse_spec(path):
    spec = json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(spec, dict):
        raise ValueError('The specification must be a JSON object')
    title = text_field(spec, 'title', 'deck', limit=34)
    subtitle = text_field(spec, 'subtitle', 'deck', limit=68)
    cover_notes = text_field(spec, 'cover_notes', 'deck', multiline=True)
    pages = spec.get('slides')
    if not isinstance(pages, list) or not pages:
        raise ValueError('deck.slides must contain at least one teaching slide')

    top_fields = ('audience', 'learning_objectives', 'duration_minutes')
    top_present = [field in spec for field in top_fields]
    activity_present = [isinstance(item, dict) and 'activity' in item for item in pages]
    legacy = not any(top_present) and not any(activity_present)
    if not legacy:
        for field, present in zip(top_fields, top_present):
            if not present:
                raise ValueError(f'deck.{field} is required when teaching metadata is used')
        for index, present in enumerate(activity_present, start=2):
            if not present:
                raise ValueError(f'page {index}.activity is required when teaching metadata is used')

        audience = text_field(spec, 'audience', 'deck')
        objectives = spec.get('learning_objectives')
        if not isinstance(objectives, list) or not 2 <= len(objectives) <= 3:
            raise ValueError('deck.learning_objectives must contain 2–3 items')
        learning_objectives = tuple(
            text_field({'text': objective}, 'text', f'deck.learning_objectives[{i}]')
            for i, objective in enumerate(objectives)
        )
        duration_minutes = spec.get('duration_minutes')
        if (isinstance(duration_minutes, bool)
                or not isinstance(duration_minutes, int)
                or duration_minutes <= 0):
            raise ValueError('deck.duration_minutes must be a positive integer')
    else:
        audience = None
        learning_objectives = None
        duration_minutes = None

    slides = []
    for i, item in enumerate(pages, start=2):
        prefix = f'page {i}'
        if not isinstance(item, dict):
            raise ValueError(f'{prefix} must be a JSON object')
        heading = text_field(item, 'title', prefix, limit=46)
        label = text_field(item, 'label', prefix, limit=20)
        notes = text_field(item, 'notes', prefix, multiline=True)
        activity = None if legacy else text_field(item, 'activity', prefix, multiline=True)
        layout = item.get('layout', 'bullets')
        if not isinstance(layout, str) or layout not in LAYOUTS:
            raise ValueError(f'{prefix}.layout must be one of {", ".join(LAYOUTS)}')
        minimum, maximum, limit = LAYOUTS[layout]
        points = item.get('points')
        if not isinstance(points, list) or not minimum <= len(points) <= maximum:
            count = str(minimum) if minimum == maximum else f'{minimum}–{maximum}'
            raise ValueError(f'{prefix}.points must contain {count} lines for {layout}')
        lines = tuple(
            text_field({'text': point}, 'text', f'{prefix}.points[{j}]', limit=limit)
            for j, point in enumerate(points)
        )
        slides.append(SlideSpec(heading, label, lines, notes, layout, activity))
    return DeckSpec(
        title, subtitle, cover_notes, tuple(slides), audience,
        learning_objectives, duration_minutes,
    )


def notes_with_metadata(notes, metadata):
    if metadata is None:
        return notes
    payload = json.dumps(
        {'version': METADATA_VERSION, **metadata},
        ensure_ascii=False,
        separators=(',', ':'),
    )
    return f'{notes}\n\n{METADATA_START}\n{payload}\n{METADATA_END}'


def parse_notes(notes):
    if METADATA_START not in notes and METADATA_END not in notes:
        return notes, None
    pattern = re.compile(
        rf'\n\n{re.escape(METADATA_START)}\n([^\n]+)\n{re.escape(METADATA_END)}\Z'
    )
    match = pattern.search(notes)
    if match is None:
        raise ValueError('PPTX verification failed: malformed teaching metadata block')
    try:
        metadata = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ValueError('PPTX verification failed: invalid teaching metadata JSON') from exc
    if not isinstance(metadata, dict) or metadata.pop('version', None) != METADATA_VERSION:
        raise ValueError('PPTX verification failed: unsupported teaching metadata version')
    return notes[:match.start()], metadata


def render(spec):
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
    from pptx.oxml.xmlchemy import OxmlElement
    from pptx.util import Inches, Pt

    ink = '10243B'
    accent = '00685E'
    muted = '435C73'
    white = 'FFFFFF'
    pale = 'E8F5F2'

    def color(value):
        return RGBColor.from_string(value)

    def rect(slide, x, y, w, h, fill):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, *(Inches(v) for v in (x, y, w, h)))
        shape.fill.solid()
        shape.fill.fore_color.rgb = color(fill)
        shape.line.fill.background()

    def textbox(slide, text, x, y, w, h, size, fg, bold=False, *, centered=False):
        shape = slide.shapes.add_textbox(*(Inches(v) for v in (x, y, w, h)))
        frame = shape.text_frame
        frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
        frame.word_wrap = True
        frame.auto_size = MSO_AUTO_SIZE.NONE
        frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        paragraph = frame.paragraphs[0]
        paragraph.alignment = PP_ALIGN.CENTER if centered else PP_ALIGN.LEFT
        run = paragraph.add_run()
        run.text = text
        run.font.name = 'Arial'
        east_asian = OxmlElement('a:ea')
        east_asian.set('typeface', 'Microsoft YaHei')
        run.font._element.append(east_asian)
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color(fg)
        return shape

    def page(background, notes):
        slide = deck.slides.add_slide(deck.slide_layouts[6])
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = color(background)
        slide.notes_slide.notes_text_frame.text = notes
        return slide

    deck = Presentation()
    deck.slide_width, deck.slide_height = Inches(40 / 3), Inches(7.5)
    deck.core_properties.title = spec.title
    titles = []
    cover_metadata = None
    if spec.has_teaching_metadata:
        cover_metadata = {
            'kind': 'deck',
            'audience': spec.audience,
            'learning_objectives': list(spec.learning_objectives),
            'duration_minutes': spec.duration_minutes,
        }
    cover = page('10243B', notes_with_metadata(spec.cover_notes, cover_metadata))
    rect(cover, 0.85, 2.03, 0.85, 0.07, '4DDCC0')
    titles.append(textbox(cover, spec.title, 0.85, 2.32, 11.5, 1.05, 43, 'FFFFFF', True).shape_id)
    textbox(cover, spec.subtitle, 0.88, 3.7, 11.5, 0.8, 23, 'BCD3E5')
    for i, slide_spec in enumerate(spec.slides, start=2):
        heading = slide_spec.title
        label = slide_spec.label
        points = slide_spec.points
        layout = slide_spec.layout
        metadata = None
        if spec.has_teaching_metadata:
            metadata = {'kind': 'slide', 'activity': slide_spec.activity}
        slide = page(white, notes_with_metadata(slide_spec.notes, metadata))
        textbox(slide, label, 0.85, 0.48, 9.0, 0.34, 16, accent, True)
        titles.append(textbox(slide, heading, 0.85, 0.96, 11.5, 1.05, 34, ink, True).shape_id)
        rect(slide, 0.85, 2.06, 11.63, 0.02, 'D8E2E8')
        if layout == 'focus':
            rect(slide, 0.85, 2.65, 11.63, 2.75, pale)
            textbox(slide, points[0], 1.45, 2.83, 10.43, 2.4, 32, ink, True, centered=True)
        elif layout == 'compare':
            for j, line in enumerate(points):
                x = 0.85 + 5.98 * j
                rect(slide, x, 2.62, 5.65, 2.9, pale if j else 'F0F4F7')
                textbox(slide, line, x + 0.32, 2.82, 5.01, 2.5, 23, ink)
        elif layout == 'practice':
            rect(slide, 0.85, 2.35, 11.63, 3.65, pale)
            textbox(slide, points[0], 1.18, 2.6, 10.95, 1.1, 29, ink, True)
            for j, line in enumerate(points[1:]):
                textbox(slide, line, 1.18, 3.8 + 0.91 * j, 10.95, 0.82, 23, ink)
        else:
            for j, line in enumerate(points):
                y = 2.27 + 1.04 * j
                if layout == 'steps':
                    textbox(slide, f'{j + 1:02d}', 0.85, y, 0.65, 0.87, 21, accent, True)
                else:
                    rect(slide, 0.91, y + 0.39, 0.10, 0.10, accent)
                textbox(slide, line, 1.6, y, 10.78, 0.87, 23, ink)
        textbox(slide, f'{i:02d} / {len(spec.slides) + 1:02d}', 11.14, 6.85, 1.3, 0.34, 14, muted)

    stream = io.BytesIO()
    deck.save(stream)
    stream.seek(0)
    reopened = Presentation(stream)
    expected = [(spec.title, spec.cover_notes, cover_metadata)] + [
        (
            slide.title,
            slide.notes,
            {'kind': 'slide', 'activity': slide.activity}
            if spec.has_teaching_metadata else None,
        )
        for slide in spec.slides
    ]
    if len(reopened.slides) != len(expected):
        raise ValueError('PPTX verification failed: incorrect slide count')
    for i, (slide, (heading, notes, metadata), shape_id) in enumerate(
            zip(reopened.slides, expected, titles), 1):
        saved_title = next(
            (shape.text for shape in slide.shapes
             if shape.shape_id == shape_id and shape.has_text_frame),
            None,
        )
        saved_notes_frame = slide.notes_slide.notes_text_frame
        if saved_notes_frame is None:
            raise ValueError(f'PPTX verification failed on page {i}: notes are missing')
        saved_notes, saved_metadata = parse_notes(saved_notes_frame.text)
        if saved_title != heading or saved_notes != notes or saved_metadata != metadata:
            raise ValueError(f'PPTX verification failed on page {i}: title, notes, or metadata differ')
    return stream.getvalue(), len(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('spec', type=Path, help='UTF-8 JSON specification')
    parser.add_argument('output', type=Path, help='new .pptx path; existing files are not overwritten')
    args = parser.parse_args()
    try:
        output = args.output
        if output.suffix.lower() != '.pptx':
            raise ValueError('Output path must end in .pptx')
        if output.exists():
            raise FileExistsError(f'Output already exists: {output}')
        data, count = render(parse_spec(args.spec))
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('xb') as file:
            file.write(data)
        print(f'PPTX verified: {count} slides — {output.resolve()}')
    except ModuleNotFoundError as exc:
        parser.exit(1, f'Could not load {exc.name}; install python-pptx and its dependencies in this Python environment.\n')
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Build failed: {exc}\n')


if __name__ == '__main__':
    main()
