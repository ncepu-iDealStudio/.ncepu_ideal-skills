package com.security.apisecurity.repository;

import com.security.apisecurity.entity.Student;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface StudentRepository extends JpaRepository<Student, Integer> {

    Optional<Student> findByAutoIdAndIsDelete(Integer autoId, boolean isDelete);

    Page<Student> findByIsDelete(boolean isDelete, Pageable pageable);

    List<Student> findByIsDelete(boolean isDelete);

    Page<Student> findByClassIdAndIsDelete(String classId, boolean isDelete, Pageable pageable);

    List<Student> findByClassIdAndIsDelete(String classId, boolean isDelete);

    Page<Student> findByCollegeIdAndIsDelete(String collegeId, boolean isDelete, Pageable pageable);

    List<Student> findByCollegeIdAndIsDelete(String collegeId, boolean isDelete);
}
