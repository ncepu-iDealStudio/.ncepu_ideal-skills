# Field line rendering template (reference)
{{ field_name_raw }} = db.Column(
    {{ sqlalchemy_type }},
    primary_key={{ is_primary_key }},
    nullable={{ nullable }},{{ default_part }}{{ info_part }}
)
