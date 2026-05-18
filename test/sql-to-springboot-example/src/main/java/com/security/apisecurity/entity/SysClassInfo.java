package com.security.apisecurity.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "sys_classInfo")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SysClassInfo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "autoID")
    private Integer autoId;

    @Column(name = "classID", length = 10)
    private String classId;

    @Column(name = "collegeID", length = 20)
    private String collegeId;

    @Column(name = "className", length = 20)
    private String className;

    @Column(name = "isDeleted")
    private Boolean isDeleted = false;

    @Column(name = "addTime")
    private LocalDateTime addTime;

    @PrePersist
    protected void onCreate() {
        if (addTime == null) {
            addTime = LocalDateTime.now();
        }
        if (isDeleted == null) {
            isDeleted = false;
        }
    }
}
