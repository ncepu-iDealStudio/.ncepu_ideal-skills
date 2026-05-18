package com.security.apisecurity.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "teacher")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Teacher {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "autoID")
    private Integer autoId;

    @Column(name = "teacherID", length = 15)
    private String teacherId;

    @Column(name = "userID", length = 22)
    private String userId;

    @Column(name = "departmentID", columnDefinition = "bigint")
    private Long departmentId;

    @Column(name = "name", length = 10)
    private String name;

    @Column(name = "email", length = 50)
    private String email;

    @Column(name = "phone", length = 15)
    private String phone;

    @Column(name = "officeAddress", length = 255)
    private String officeAddress;

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
