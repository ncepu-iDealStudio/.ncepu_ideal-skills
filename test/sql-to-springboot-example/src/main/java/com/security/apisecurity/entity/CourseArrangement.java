package com.security.apisecurity.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "course_arrangement")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class CourseArrangement {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "autoID")
    private Integer autoId;

    @Column(name = "courseID", length = 20)
    private String courseId;

    @Column(name = "termID", length = 50)
    private String termId;

    @Column(name = "classTime", length = 20)
    private String classTime;

    @Column(name = "count")
    private Integer count;

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
