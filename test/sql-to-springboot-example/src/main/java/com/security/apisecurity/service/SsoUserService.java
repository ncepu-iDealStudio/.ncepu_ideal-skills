package com.security.apisecurity.service;

import com.security.apisecurity.dto.request.SsoUserRequest;
import com.security.apisecurity.dto.response.SsoUserResponse;
import com.security.apisecurity.entity.SsoUser;
import com.security.apisecurity.exception.ResourceNotFoundException;
import com.security.apisecurity.repository.SsoUserRepository;
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
public class SsoUserService {

    private final SsoUserRepository ssoUserRepository;

    public SsoUserResponse create(SsoUserRequest request) {
        SsoUser entity = new SsoUser();
        entity.setUserId(request.getUserId());
        entity.setAccount(request.getAccount());
        entity.setPassword(request.getPassword());
        entity.setUserType(request.getUserType());
        entity.setStatus(request.getStatus());

        SsoUser saved = ssoUserRepository.save(entity);
        log.info("Created ssoUser with autoId: {}", saved.getAutoId());

        return mapToResponse(saved);
    }

    public SsoUserResponse getById(Long id) {
        SsoUser entity = findEntityById(id);
        return mapToResponse(entity);
    }

    public Page<SsoUserResponse> getList(int page, int size, String sortBy, String sortDir) {
        Sort sort = Sort.by(Sort.Direction.fromString(sortDir), sortBy);
        Pageable pageable = PageRequest.of(page, size, sort);

        Page<SsoUser> entities = ssoUserRepository.findAll(pageable);
        return entities.map(this::mapToResponse);
    }

    public SsoUserResponse update(Long id, SsoUserRequest request) {
        SsoUser entity = findEntityById(id);
        if (request.getUserId() != null) {
            entity.setUserId(request.getUserId());
        }
        if (request.getAccount() != null) {
            entity.setAccount(request.getAccount());
        }
        if (request.getPassword() != null) {
            entity.setPassword(request.getPassword());
        }
        if (request.getUserType() != null) {
            entity.setUserType(request.getUserType());
        }
        if (request.getStatus() != null) {
            entity.setStatus(request.getStatus());
        }

        SsoUser updated = ssoUserRepository.save(entity);
        log.info("Updated ssoUser with autoId: {}", updated.getAutoId());

        return mapToResponse(updated);
    }

    public void delete(Long id) {
        SsoUser entity = findEntityById(id);
        ssoUserRepository.delete(entity);
        log.info("Hard deleted ssoUser with autoId: {}", id);
    }

    private SsoUser findEntityById(Long id) {
        return ssoUserRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("SsoUser not found with autoId: " + id));
    }

    private SsoUserResponse mapToResponse(SsoUser entity) {
        return new SsoUserResponse(
                entity.getAutoId(),
                entity.getUserId(),
                entity.getAccount(),
                entity.getUserType(),
                entity.getStatus(),
                entity.getAddTime()
        );
    }
}
