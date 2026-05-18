package com.security.apisecurity.repository;

import com.security.apisecurity.entity.Admin;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface AdminRepository extends JpaRepository<Admin, Integer> {

    Optional<Admin> findByAutoIdAndIsDelete(Integer autoId, boolean isDelete);

    Page<Admin> findByIsDelete(boolean isDelete, Pageable pageable);

    List<Admin> findByIsDelete(boolean isDelete);

    Page<Admin> findByDepartmentIdAndIsDelete(Long departmentId, boolean isDelete, Pageable pageable);

    List<Admin> findByDepartmentIdAndIsDelete(Long departmentId, boolean isDelete);
}
