package com.security.apisecurity.service;

import com.security.apisecurity.dto.request.CourseArrangementRequest;
import com.security.apisecurity.dto.response.CourseArrangementResponse;
import com.security.apisecurity.entity.CourseArrangement;
import com.security.apisecurity.exception.ResourceNotFoundException;
import com.security.apisecurity.repository.CourseArrangementRepository;
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
public class CourseArrangementService {

    private final CourseArrangementRepository courseArrangementRepository;

    public CourseArrangementResponse create(CourseArrangementRequest request) {
        CourseArrangement entity = new CourseArrangement();
        entity.setCourseId(request.getCourseId());
        entity.setTermId(request.getTermId());
        entity.setClassTime(request.getClassTime());
        entity.setCount(request.getCount());

        CourseArrangement saved = courseArrangementRepository.save(entity);
        log.info("Created courseArrangement with autoId: {}", saved.getAutoId());

        return mapToResponse(saved);
    }

    public CourseArrangementResponse getById(Integer id) {
        CourseArrangement entity = findEntityById(id);
        return mapToResponse(entity);
    }

    public Page<CourseArrangementResponse> getList(int page, int size, String sortBy, String sortDir) {
        Sort sort = Sort.by(Sort.Direction.fromString(sortDir), sortBy);
        Pageable pageable = PageRequest.of(page, size, sort);

        Page<CourseArrangement> entities = courseArrangementRepository.findByIsDelete(false, pageable);
        return entities.map(this::mapToResponse);
    }

    public CourseArrangementResponse update(Integer id, CourseArrangementRequest request) {
        CourseArrangement entity = findEntityById(id);
        if (request.getCourseId() != null) {
            entity.setCourseId(request.getCourseId());
        }
        if (request.getTermId() != null) {
            entity.setTermId(request.getTermId());
        }
        if (request.getClassTime() != null) {
            entity.setClassTime(request.getClassTime());
        }
        if (request.getCount() != null) {
            entity.setCount(request.getCount());
        }

        CourseArrangement updated = courseArrangementRepository.save(entity);
        log.info("Updated courseArrangement with autoId: {}", updated.getAutoId());

        return mapToResponse(updated);
    }

    public void delete(Integer id) {
        CourseArrangement entity = findEntityById(id);
        entity.setIsDelete(true);
        courseArrangementRepository.save(entity);
        log.info("Soft deleted courseArrangement with autoId: {}", id);
    }

    private CourseArrangement findEntityById(Integer id) {
        return courseArrangementRepository.findByAutoIdAndIsDelete(id, false)
                .orElseThrow(() -> new ResourceNotFoundException("CourseArrangement not found with autoId: " + id));
    }

    private CourseArrangementResponse mapToResponse(CourseArrangement entity) {
        return new CourseArrangementResponse(
                entity.getAutoId(),
                entity.getCourseId(),
                entity.getTermId(),
                entity.getClassTime(),
                entity.getCount(),
                entity.getIsDelete(),
                entity.getAddTime()
        );
    }
}
