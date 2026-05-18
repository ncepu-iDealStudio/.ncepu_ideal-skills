package com.security.apisecurity.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "student_selected_course")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class StudentSelectedCourse {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "autoID")
    private Integer autoId;

    @Column(name = "studentID", length = 20, nullable = false)
    private String studentId;

    @Column(name = "courseID", length = 15, nullable = false)
    private String courseId;

    @Column(name = "score")
    private Integer score;

    @Column(name = "isDelete")
    private Boolean isDelete = false;

    @Column(name = "addTime")
    private LocalDateTime addTime;

    @PrePersist
    protected void onCreate() {
        if (addTime == null) {
            addTime = LocalDateTime.now();
        }
        if (isDelete == null) {
            isDelete = false;
        }
    }
}
