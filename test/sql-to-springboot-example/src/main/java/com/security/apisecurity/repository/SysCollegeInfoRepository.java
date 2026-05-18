package com.security.apisecurity.repository;

import com.security.apisecurity.entity.SysCollegeInfo;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface SysCollegeInfoRepository extends JpaRepository<SysCollegeInfo, Long> {

    Optional<SysCollegeInfo> findByAutoIdAndIsDelete(Long autoId, boolean isDelete);

    Page<SysCollegeInfo> findByIsDelete(boolean isDelete, Pageable pageable);

    List<SysCollegeInfo> findByIsDelete(boolean isDelete);
}
