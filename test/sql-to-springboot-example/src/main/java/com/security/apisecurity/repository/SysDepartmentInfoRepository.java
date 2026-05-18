package com.security.apisecurity.repository;

import com.security.apisecurity.entity.SysDepartmentInfo;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface SysDepartmentInfoRepository extends JpaRepository<SysDepartmentInfo, Long> {

    Optional<SysDepartmentInfo> findByAutoIdAndIsDeleted(Long autoId, boolean isDeleted);

    Page<SysDepartmentInfo> findByIsDeleted(boolean isDeleted, Pageable pageable);

    List<SysDepartmentInfo> findByIsDeleted(boolean isDeleted);

    Page<SysDepartmentInfo> findByCollegeIdAndIsDeleted(String collegeId, boolean isDeleted, Pageable pageable);

    List<SysDepartmentInfo> findByCollegeIdAndIsDeleted(String collegeId, boolean isDeleted);

    Page<SysDepartmentInfo> findByParentDepartmentIdAndIsDeleted(Long parentDepartmentId, boolean isDeleted, Pageable pageable);

    List<SysDepartmentInfo> findByParentDepartmentIdAndIsDeleted(Long parentDepartmentId, boolean isDeleted);
}
