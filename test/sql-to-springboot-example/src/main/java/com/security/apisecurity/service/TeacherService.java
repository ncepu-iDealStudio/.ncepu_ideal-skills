package com.security.apisecurity.service;

import com.security.apisecurity.dto.request.TeacherRequest;
import com.security.apisecurity.dto.response.TeacherResponse;
import com.security.apisecurity.entity.Teacher;
import com.security.apisecurity.exception.ResourceNotFoundException;
import com.security.apisecurity.repository.TeacherRepository;
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
public class TeacherService {

    private final TeacherRepository teacherRepository;

    public TeacherResponse create(TeacherRequest request) {
        Teacher entity = new Teacher();
        entity.setTeacherId(request.getTeacherId());
        entity.setUserId(request.getUserId());
        entity.setDepartmentId(request.getDepartmentId());
        entity.setName(request.getName());
        entity.setEmail(request.getEmail());
        entity.setPhone(request.getPhone());
        entity.setOfficeAddress(request.getOfficeAddress());

        Teacher saved = teacherRepository.save(entity);
        log.info("Created teacher with autoId: {}", saved.getAutoId());

        return mapToResponse(saved);
    }

    public TeacherResponse getById(Integer id) {
        Teacher entity = findEntityById(id);
        return mapToResponse(entity);
    }

    public Page<TeacherResponse> getList(int page, int size, String sortBy, String sortDir) {
        Sort sort = Sort.by(Sort.Direction.fromString(sortDir), sortBy);
        Pageable pageable = PageRequest.of(page, size, sort);

        Page<Teacher> entities = teacherRepository.findByIsDelete(false, pageable);
        return entities.map(this::mapToResponse);
    }

    public TeacherResponse update(Integer id, TeacherRequest request) {
        Teacher entity = findEntityById(id);
        if (request.getTeacherId() != null) {
            entity.setTeacherId(request.getTeacherId());
        }
        if (request.getUserId() != null) {
            entity.setUserId(request.getUserId());
        }
        if (request.getDepartmentId() != null) {
            entity.setDepartmentId(request.getDepartmentId());
        }
        if (request.getName() != null) {
            entity.setName(request.getName());
        }
        if (request.getEmail() != null) {
            entity.setEmail(request.getEmail());
        }
        if (request.getPhone() != null) {
            entity.setPhone(request.getPhone());
        }
        if (request.getOfficeAddress() != null) {
            entity.setOfficeAddress(request.getOfficeAddress());
        }

        Teacher updated = teacherRepository.save(entity);
        log.info("Updated teacher with autoId: {}", updated.getAutoId());

        return mapToResponse(updated);
    }

    public void delete(Integer id) {
        Teacher entity = findEntityById(id);
        entity.setIsDelete(true);
        teacherRepository.save(entity);
        log.info("Soft deleted teacher with autoId: {}", id);
    }

    private Teacher findEntityById(Integer id) {
        return teacherRepository.findByAutoIdAndIsDelete(id, false)
                .orElseThrow(() -> new ResourceNotFoundException("Teacher not found with autoId: " + id));
    }

    private TeacherResponse mapToResponse(Teacher entity) {
        return new TeacherResponse(
                entity.getAutoId(),
                entity.getTeacherId(),
                entity.getUserId(),
                entity.getDepartmentId(),
                entity.getName(),
                entity.getEmail(),
                entity.getPhone(),
                entity.getOfficeAddress(),
                entity.getIsDelete(),
                entity.getAddTime()
        );
    }
}
