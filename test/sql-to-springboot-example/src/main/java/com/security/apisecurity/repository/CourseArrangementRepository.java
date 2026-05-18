package com.security.apisecurity.repository;

import com.security.apisecurity.entity.CourseArrangement;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CourseArrangementRepository extends JpaRepository<CourseArrangement, Integer> {

    Optional<CourseArrangement> findByAutoIdAndIsDelete(Integer autoId, boolean isDelete);

    Page<CourseArrangement> findByIsDelete(boolean isDelete, Pageable pageable);

    List<CourseArrangement> findByIsDelete(boolean isDelete);

    Page<CourseArrangement> findByCourseIdAndIsDelete(String courseId, boolean isDelete, Pageable pageable);

    List<CourseArrangement> findByCourseIdAndIsDelete(String courseId, boolean isDelete);
}
