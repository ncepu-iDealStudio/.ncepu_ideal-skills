package com.security.apisecurity.service;

import com.security.apisecurity.dto.request.SysCollegeInfoRequest;
import com.security.apisecurity.dto.response.SysCollegeInfoResponse;
import com.security.apisecurity.entity.SysCollegeInfo;
import com.security.apisecurity.exception.ResourceNotFoundException;
import com.security.apisecurity.repository.SysCollegeInfoRepository;
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
public class SysCollegeInfoService {

    private final SysCollegeInfoRepository sysCollegeInfoRepository;

    public SysCollegeInfoResponse create(SysCollegeInfoRequest request) {
        SysCollegeInfo entity = new SysCollegeInfo();
        entity.setCollegeId(request.getCollegeId());
        entity.setCollegeName(request.getCollegeName());

        SysCollegeInfo saved = sysCollegeInfoRepository.save(entity);
        log.info("Created sysCollegeInfo with autoId: {}", saved.getAutoId());

        return mapToResponse(saved);
    }

    public SysCollegeInfoResponse getById(Long id) {
        SysCollegeInfo entity = findEntityById(id);
        return mapToResponse(entity);
    }

    public Page<SysCollegeInfoResponse> getList(int page, int size, String sortBy, String sortDir) {
        Sort sort = Sort.by(Sort.Direction.fromString(sortDir), sortBy);
        Pageable pageable = PageRequest.of(page, size, sort);

        Page<SysCollegeInfo> entities = sysCollegeInfoRepository.findByIsDelete(false, pageable);
        return entities.map(this::mapToResponse);
    }

    public SysCollegeInfoResponse update(Long id, SysCollegeInfoRequest request) {
        SysCollegeInfo entity = findEntityById(id);
        if (request.getCollegeId() != null) {
            entity.setCollegeId(request.getCollegeId());
        }
        if (request.getCollegeName() != null) {
            entity.setCollegeName(request.getCollegeName());
        }

        SysCollegeInfo updated = sysCollegeInfoRepository.save(entity);
        log.info("Updated sysCollegeInfo with autoId: {}", updated.getAutoId());

        return mapToResponse(updated);
    }

    public void delete(Long id) {
        SysCollegeInfo entity = findEntityById(id);
        entity.setIsDelete(true);
        sysCollegeInfoRepository.save(entity);
        log.info("Soft deleted sysCollegeInfo with autoId: {}", id);
    }

    private SysCollegeInfo findEntityById(Long id) {
        return sysCollegeInfoRepository.findByAutoIdAndIsDelete(id, false)
                .orElseThrow(() -> new ResourceNotFoundException("SysCollegeInfo not found with autoId: " + id));
    }

    private SysCollegeInfoResponse mapToResponse(SysCollegeInfo entity) {
        return new SysCollegeInfoResponse(
                entity.getAutoId(),
                entity.getCollegeId(),
                entity.getCollegeName(),
                entity.getIsDelete(),
                entity.getAddTime()
        );
    }
}
