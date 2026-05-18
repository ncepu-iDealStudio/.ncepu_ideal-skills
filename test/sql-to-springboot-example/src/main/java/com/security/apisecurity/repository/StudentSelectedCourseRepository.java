package com.security.apisecurity.repository;

import com.security.apisecurity.entity.StudentSelectedCourse;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface StudentSelectedCourseRepository extends JpaRepository<StudentSelectedCourse, Integer> {

    Optional<StudentSelectedCourse> findByAutoIdAndIsDelete(Integer autoId, boolean isDelete);

    Page<StudentSelectedCourse> findByIsDelete(boolean isDelete, Pageable pageable);

    List<StudentSelectedCourse> findByIsDelete(boolean isDelete);

    Page<StudentSelectedCourse> findByStudentIdAndIsDelete(String studentId, boolean isDelete, Pageable pageable);

    List<StudentSelectedCourse> findByStudentIdAndIsDelete(String studentId, boolean isDelete);

    Page<StudentSelectedCourse> findByCourseIdAndIsDelete(String courseId, boolean isDelete, Pageable pageable);

    List<StudentSelectedCourse> findByCourseIdAndIsDelete(String courseId, boolean isDelete);
}
