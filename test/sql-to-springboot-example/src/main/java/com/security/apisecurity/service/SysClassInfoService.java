package com.security.apisecurity.service;

import com.security.apisecurity.dto.request.SysClassInfoRequest;
import com.security.apisecurity.dto.response.SysClassInfoResponse;
import com.security.apisecurity.entity.SysClassInfo;
import com.security.apisecurity.exception.ResourceNotFoundException;
import com.security.apisecurity.repository.SysClassInfoRepository;
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
public class SysClassInfoService {

    private final SysClassInfoRepository sysClassInfoRepository;

    public SysClassInfoResponse create(SysClassInfoRequest request) {
        SysClassInfo entity = new SysClassInfo();
        entity.setClassId(request.getClassId());
        entity.setCollegeId(request.getCollegeId());
        entity.setClassName(request.getClassName());

        SysClassInfo saved = sysClassInfoRepository.save(entity);
        log.info("Created sysClassInfo with autoId: {}", saved.getAutoId());

        return mapToResponse(saved);
    }

    public SysClassInfoResponse getById(Integer id) {
        SysClassInfo entity = findEntityById(id);
        return mapToResponse(entity);
    }

    public Page<SysClassInfoResponse> getList(int page, int size, String sortBy, String sortDir) {
        Sort sort = Sort.by(Sort.Direction.fromString(sortDir), sortBy);
        Pageable pageable = PageRequest.of(page, size, sort);

        Page<SysClassInfo> entities = sysClassInfoRepository.findByIsDeleted(false, pageable);
        return entities.map(this::mapToResponse);
    }

    public SysClassInfoResponse update(Integer id, SysClassInfoRequest request) {
        SysClassInfo entity = findEntityById(id);
        if (request.getClassId() != null) {
            entity.setClassId(request.getClassId());
        }
        if (request.getCollegeId() != null) {
            entity.setCollegeId(request.getCollegeId());
        }
        if (request.getClassName() != null) {
            entity.setClassName(request.getClassName());
        }

        SysClassInfo updated = sysClassInfoRepository.save(entity);
        log.info("Updated sysClassInfo with autoId: {}", updated.getAutoId());

        return mapToResponse(updated);
    }

    public void delete(Integer id) {
        SysClassInfo entity = findEntityById(id);
        entity.setIsDeleted(true);
        sysClassInfoRepository.save(entity);
        log.info("Soft deleted sysClassInfo with autoId: {}", id);
    }

    private SysClassInfo findEntityById(Integer id) {
        return sysClassInfoRepository.findByAutoIdAndIsDeleted(id, false)
                .orElseThrow(() -> new ResourceNotFoundException("SysClassInfo not found with autoId: " + id));
    }

    private SysClassInfoResponse mapToResponse(SysClassInfo entity) {
        return new SysClassInfoResponse(
                entity.getAutoId(),
                entity.getClassId(),
                entity.getCollegeId(),
                entity.getClassName(),
                entity.getIsDeleted(),
                entity.getAddTime()
        );
    }
}
