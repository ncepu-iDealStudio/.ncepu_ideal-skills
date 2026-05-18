package com.security.apisecurity.service;

import com.security.apisecurity.dto.request.StudentSelectedCourseRequest;
import com.security.apisecurity.dto.response.StudentSelectedCourseResponse;
import com.security.apisecurity.entity.StudentSelectedCourse;
import com.security.apisecurity.exception.ResourceNotFoundException;
import com.security.apisecurity.repository.StudentSelectedCourseRepository;
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
public class StudentSelectedCourseService {

    private final StudentSelectedCourseRepository studentSelectedCourseRepository;

    public StudentSelectedCourseResponse create(StudentSelectedCourseRequest request) {
        StudentSelectedCourse entity = new StudentSelectedCourse();
        entity.setStudentId(request.getStudentId());
        entity.setCourseId(request.getCourseId());
        entity.setScore(request.getScore());

        StudentSelectedCourse saved = studentSelectedCourseRepository.save(entity);
        log.info("Created studentSelectedCourse with autoId: {}", saved.getAutoId());

        return mapToResponse(saved);
    }

    public StudentSelectedCourseResponse getById(Integer id) {
        StudentSelectedCourse entity = findEntityById(id);
        return mapToResponse(entity);
    }

    public Page<StudentSelectedCourseResponse> getList(int page, int size, String sortBy, String sortDir) {
        Sort sort = Sort.by(Sort.Direction.fromString(sortDir), sortBy);
        Pageable pageable = PageRequest.of(page, size, sort);

        Page<StudentSelectedCourse> entities = studentSelectedCourseRepository.findByIsDelete(false, pageable);
        return entities.map(this::mapToResponse);
    }

    public StudentSelectedCourseResponse update(Integer id, StudentSelectedCourseRequest request) {
        StudentSelectedCourse entity = findEntityById(id);
        if (request.getStudentId() != null) {
            entity.setStudentId(request.getStudentId());
        }
        if (request.getCourseId() != null) {
            entity.setCourseId(request.getCourseId());
        }
        if (request.getScore() != null) {
            entity.setScore(request.getScore());
        }

        StudentSelectedCourse updated = studentSelectedCourseRepository.save(entity);
        log.info("Updated studentSelectedCourse with autoId: {}", updated.getAutoId());

        return mapToResponse(updated);
    }

    public void delete(Integer id) {
        StudentSelectedCourse entity = findEntityById(id);
        entity.setIsDelete(true);
        studentSelectedCourseRepository.save(entity);
        log.info("Soft deleted studentSelectedCourse with autoId: {}", id);
    }

    private StudentSelectedCourse findEntityById(Integer id) {
        return studentSelectedCourseRepository.findByAutoIdAndIsDelete(id, false)
                .orElseThrow(() -> new ResourceNotFoundException("StudentSelectedCourse not found with autoId: " + id));
    }

    private StudentSelectedCourseResponse mapToResponse(StudentSelectedCourse entity) {
        return new StudentSelectedCourseResponse(
                entity.getAutoId(),
                entity.getStudentId(),
                entity.getCourseId(),
                entity.getScore(),
                entity.getIsDelete(),
                entity.getAddTime()
        );
    }
}
