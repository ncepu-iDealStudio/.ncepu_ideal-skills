package com.security.apisecurity.service;

import com.security.apisecurity.dto.request.CourseRequest;
import com.security.apisecurity.dto.response.CourseResponse;
import com.security.apisecurity.entity.Course;
import com.security.apisecurity.exception.ResourceNotFoundException;
import com.security.apisecurity.repository.CourseRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@Transactional
@RequiredArgsConstructor
public class CourseService {

    private final CourseRepository courseRepository;

    public CourseResponse create(CourseRequest request) {
        Course entity = new Course();
        entity.setCourseId(request.getCourseId());
        entity.setCourseName(request.getCourseName());
        entity.setTeacherId(request.getTeacherId());
        entity.setCredit(request.getCredit());

        Course saved = courseRepository.save(entity);
        log.info("Created course with autoId: {}", saved.getAutoId());

        return mapToResponse(saved);
    }

    public CourseResponse getById(Integer id) {
        Course entity = findEntityById(id);
        return mapToResponse(entity);
    }

    public Page<CourseResponse> getList(int page, int size, String sortBy, String sortDir) {
        Sort sort = Sort.by(Sort.Direction.fromString(sortDir), sortBy);
        Pageable pageable = PageRequest.of(page, size, sort);

        Page<Course> entities = courseRepository.findByIsDelete(false, pageable);
        return entities.map(this::mapToResponse);
    }

    public CourseResponse update(Integer id, CourseRequest request) {
        Course entity = findEntityById(id);
        if (request.getCourseId() != null) {
            entity.setCourseId(request.getCourseId());
        }
        if (request.getCourseName() != null) {
            entity.setCourseName(request.getCourseName());
        }
        if (request.getTeacherId() != null) {
            entity.setTeacherId(request.getTeacherId());
        }
        if (request.getCredit() != null) {
            entity.setCredit(request.getCredit());
        }

        Course updated = courseRepository.save(entity);
        log.info("Updated course with autoId: {}", updated.getAutoId());

        return mapToResponse(updated);
    }

    public void delete(Integer id) {
        Course entity = findEntityById(id);
        entity.setIsDelete(true);
        courseRepository.save(entity);
        log.info("Soft deleted course with autoId: {}", id);
    }

    private Course findEntityById(Integer id) {
        return courseRepository.findByAutoIdAndIsDelete(id, false)
                .orElseThrow(() -> new ResourceNotFoundException("Course not found with autoId: " + id));
    }

    private CourseResponse mapToResponse(Course entity) {
        return new CourseResponse(
                entity.getAutoId(),
                entity.getCourseId(),
                entity.getCourseName(),
                entity.getTeacherId(),
                entity.getCredit(),
                entity.getIsDelete(),
                entity.getAddTime()
        );
    }
}
