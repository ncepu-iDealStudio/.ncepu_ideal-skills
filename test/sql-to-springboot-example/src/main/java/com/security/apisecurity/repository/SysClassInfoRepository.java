package com.security.apisecurity.repository;

import com.security.apisecurity.entity.SysClassInfo;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface SysClassInfoRepository extends JpaRepository<SysClassInfo, Integer> {

    Optional<SysClassInfo> findByAutoIdAndIsDeleted(Integer autoId, boolean isDeleted);

    Page<SysClassInfo> findByIsDeleted(boolean isDeleted, Pageable pageable);

    List<SysClassInfo> findByIsDeleted(boolean isDeleted);

    Page<SysClassInfo> findByCollegeIdAndIsDeleted(String collegeId, boolean isDeleted, Pageable pageable);

    List<SysClassInfo> findByCollegeIdAndIsDeleted(String collegeId, boolean isDeleted);
}
