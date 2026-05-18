package com.security.apisecurity.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "student")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "autoID")
    private Integer autoId;

    @Column(name = "studentID", length = 20)
    private String studentId;

    @Column(name = "userID", length = 22)
    private String userId;

    @Column(name = "classID", length = 10)
    private String classId;

    @Column(name = "collegeID", length = 20)
    private String collegeId;

    @Column(name = "name", length = 20)
    private String name;

    @Column(name = "phoneNumber", length = 500)
    private String phoneNumber;

    @Column(name = "age")
    private Integer age;

    @Column(name = "agenda", length = 10)
    private String agenda;

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
