package com.security.apisecurity.service;

import com.security.apisecurity.dto.request.AdminRequest;
import com.security.apisecurity.dto.response.AdminResponse;
import com.security.apisecurity.entity.Admin;
import com.security.apisecurity.exception.ResourceNotFoundException;
import com.security.apisecurity.repository.AdminRepository;
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
public class AdminService {

    private final AdminRepository adminRepository;

    public AdminResponse create(AdminRequest request) {
        Admin entity = new Admin();
        entity.setAdminId(request.getAdminId());
        entity.setUserId(request.getUserId());
        entity.setDepartmentId(request.getDepartmentId());
        entity.setName(request.getName());
        entity.setEmail(request.getEmail());
        entity.setPhone(request.getPhone());
        entity.setOfficeAddress(request.getOfficeAddress());

        Admin saved = adminRepository.save(entity);
        log.info("Created admin with autoId: {}", saved.getAutoId());

        return mapToResponse(saved);
    }

    public AdminResponse getById(Integer id) {
        Admin entity = findEntityById(id);
        return mapToResponse(entity);
    }

    public Page<AdminResponse> getList(int page, int size, String sortBy, String sortDir) {
        Sort sort = Sort.by(Sort.Direction.fromString(sortDir), sortBy);
        Pageable pageable = PageRequest.of(page, size, sort);

        Page<Admin> entities = adminRepository.findByIsDelete(false, pageable);
        return entities.map(this::mapToResponse);
    }

    public AdminResponse update(Integer id, AdminRequest request) {
        Admin entity = findEntityById(id);
        if (request.getAdminId() != null) {
            entity.setAdminId(request.getAdminId());
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

        Admin updated = adminRepository.save(entity);
        log.info("Updated admin with autoId: {}", updated.getAutoId());

        return mapToResponse(updated);
    }

    public void delete(Integer id) {
        Admin entity = findEntityById(id);
        entity.setIsDelete(true);
        adminRepository.save(entity);
        log.info("Soft deleted admin with autoId: {}", id);
    }

    private Admin findEntityById(Integer id) {
        return adminRepository.findByAutoIdAndIsDelete(id, false)
                .orElseThrow(() -> new ResourceNotFoundException("Admin not found with autoId: " + id));
    }

    private AdminResponse mapToResponse(Admin entity) {
        return new AdminResponse(
                entity.getAutoId(),
                entity.getAdminId(),
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
