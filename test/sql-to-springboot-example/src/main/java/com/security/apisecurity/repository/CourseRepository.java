package com.security.apisecurity.repository;

import com.security.apisecurity.entity.Course;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CourseRepository extends JpaRepository<Course, Integer> {

    Optional<Course> findByAutoIdAndIsDelete(Integer autoId, boolean isDelete);

    Page<Course> findByIsDelete(boolean isDelete, Pageable pageable);

    List<Course> findByIsDelete(boolean isDelete);

    Page<Course> findByTeacherIdAndIsDelete(String teacherId, boolean isDelete, Pageable pageable);

    List<Course> findByTeacherIdAndIsDelete(String teacherId, boolean isDelete);
}
