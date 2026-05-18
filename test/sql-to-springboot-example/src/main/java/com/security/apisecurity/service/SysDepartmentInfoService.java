package com.security.apisecurity.service;

import com.security.apisecurity.dto.request.SysDepartmentInfoRequest;
import com.security.apisecurity.dto.response.SysDepartmentInfoResponse;
import com.security.apisecurity.entity.SysDepartmentInfo;
import com.security.apisecurity.exception.ResourceNotFoundException;
import com.security.apisecurity.repository.SysDepartmentInfoRepository;
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
public class SysDepartmentInfoService {

    private final SysDepartmentInfoRepository sysDepartmentInfoRepository;

    public SysDepartmentInfoResponse create(SysDepartmentInfoRequest request) {
        SysDepartmentInfo entity = new SysDepartmentInfo();
        entity.setDepartmentId(request.getDepartmentId());
        entity.setParentDepartmentId(request.getParentDepartmentId());
        entity.setCollegeId(request.getCollegeId());
        entity.setDepartmentName(request.getDepartmentName());
        entity.setDepartmentType(request.getDepartmentType());

        SysDepartmentInfo saved = sysDepartmentInfoRepository.save(entity);
        log.info("Created sysDepartmentInfo with autoId: {}", saved.getAutoId());

        return mapToResponse(saved);
    }

    public SysDepartmentInfoResponse getById(Long id) {
        SysDepartmentInfo entity = findEntityById(id);
        return mapToResponse(entity);
    }

    public Page<SysDepartmentInfoResponse> getList(int page, int size, String sortBy, String sortDir) {
        Sort sort = Sort.by(Sort.Direction.fromString(sortDir), sortBy);
        Pageable pageable = PageRequest.of(page, size, sort);

        Page<SysDepartmentInfo> entities = sysDepartmentInfoRepository.findByIsDeleted(false, pageable);
        return entities.map(this::mapToResponse);
    }

    public SysDepartmentInfoResponse update(Long id, SysDepartmentInfoRequest request) {
        SysDepartmentInfo entity = findEntityById(id);
        if (request.getDepartmentId() != null) {
            entity.setDepartmentId(request.getDepartmentId());
        }
        if (request.getParentDepartmentId() != null) {
            entity.setParentDepartmentId(request.getParentDepartmentId());
        }
        if (request.getCollegeId() != null) {
            entity.setCollegeId(request.getCollegeId());
        }
        if (request.getDepartmentName() != null) {
            entity.setDepartmentName(request.getDepartmentName());
        }
        if (request.getDepartmentType() != null) {
            entity.setDepartmentType(request.getDepartmentType());
        }

        SysDepartmentInfo updated = sysDepartmentInfoRepository.save(entity);
        log.info("Updated sysDepartmentInfo with autoId: {}", updated.getAutoId());

        return mapToResponse(updated);
    }

    public void delete(Long id) {
        SysDepartmentInfo entity = findEntityById(id);
        entity.setIsDeleted(true);
        sysDepartmentInfoRepository.save(entity);
        log.info("Soft deleted sysDepartmentInfo with autoId: {}", id);
    }

    private SysDepartmentInfo findEntityById(Long id) {
        return sysDepartmentInfoRepository.findByAutoIdAndIsDeleted(id, false)
                .orElseThrow(() -> new ResourceNotFoundException("SysDepartmentInfo not found with autoId: " + id));
    }

    private SysDepartmentInfoResponse mapToResponse(SysDepartmentInfo entity) {
        return new SysDepartmentInfoResponse(
                entity.getAutoId(),
                entity.getDepartmentId(),
                entity.getParentDepartmentId(),
                entity.getCollegeId(),
                entity.getDepartmentName(),
                entity.getDepartmentType(),
                entity.getIsDeleted(),
                entity.getAddTime()
        );
    }
}
