package com.security.apisecurity.service;

import com.security.apisecurity.dto.request.StudentRequest;
import com.security.apisecurity.dto.response.StudentResponse;
import com.security.apisecurity.entity.Student;
import com.security.apisecurity.exception.ResourceNotFoundException;
import com.security.apisecurity.repository.StudentRepository;
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
public class StudentService {

    private final StudentRepository studentRepository;

    public StudentResponse create(StudentRequest request) {
        Student entity = new Student();
        entity.setStudentId(request.getStudentId());
        entity.setUserId(request.getUserId());
        entity.setClassId(request.getClassId());
        entity.setCollegeId(request.getCollegeId());
        entity.setName(request.getName());
        entity.setPhoneNumber(request.getPhoneNumber());
        entity.setAge(request.getAge());
        entity.setAgenda(request.getAgenda());

        Student saved = studentRepository.save(entity);
        log.info("Created student with autoId: {}", saved.getAutoId());

        return mapToResponse(saved);
    }

    public StudentResponse getById(Integer id) {
        Student entity = findEntityById(id);
        return mapToResponse(entity);
    }

    public Page<StudentResponse> getList(int page, int size, String sortBy, String sortDir) {
        Sort sort = Sort.by(Sort.Direction.fromString(sortDir), sortBy);
        Pageable pageable = PageRequest.of(page, size, sort);

        Page<Student> entities = studentRepository.findByIsDelete(false, pageable);
        return entities.map(this::mapToResponse);
    }

    public StudentResponse update(Integer id, StudentRequest request) {
        Student entity = findEntityById(id);
        if (request.getStudentId() != null) {
            entity.setStudentId(request.getStudentId());
        }
        if (request.getUserId() != null) {
            entity.setUserId(request.getUserId());
        }
        if (request.getClassId() != null) {
            entity.setClassId(request.getClassId());
        }
        if (request.getCollegeId() != null) {
            entity.setCollegeId(request.getCollegeId());
        }
        if (request.getName() != null) {
            entity.setName(request.getName());
        }
        if (request.getPhoneNumber() != null) {
            entity.setPhoneNumber(request.getPhoneNumber());
        }
        if (request.getAge() != null) {
            entity.setAge(request.getAge());
        }
        if (request.getAgenda() != null) {
            entity.setAgenda(request.getAgenda());
        }

        Student updated = studentRepository.save(entity);
        log.info("Updated student with autoId: {}", updated.getAutoId());

        return mapToResponse(updated);
    }

    public void delete(Integer id) {
        Student entity = findEntityById(id);
        entity.setIsDelete(true);
        studentRepository.save(entity);
        log.info("Soft deleted student with autoId: {}", id);
    }

    private Student findEntityById(Integer id) {
        return studentRepository.findByAutoIdAndIsDelete(id, false)
                .orElseThrow(() -> new ResourceNotFoundException("Student not found with autoId: " + id));
    }

    private StudentResponse mapToResponse(Student entity) {
        return new StudentResponse(
                entity.getAutoId(),
                entity.getStudentId(),
                entity.getUserId(),
                entity.getClassId(),
                entity.getCollegeId(),
                entity.getName(),
                entity.getPhoneNumber(),
                entity.getAge(),
                entity.getAgenda(),
                entity.getIsDelete(),
                entity.getAddTime()
        );
    }
}
