package com.security.apisecurity.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "sys_departmentInfo")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SysDepartmentInfo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "autoID")
    private Long autoId;

    @Column(name = "departmentID", columnDefinition = "bigint")
    private Long departmentId;

    @Column(name = "parentDepartmentID", columnDefinition = "bigint")
    private Long parentDepartmentId = 0L;

    @Column(name = "collegeID", length = 20)
    private String collegeId;

    @Column(name = "departmentName", length = 255)
    private String departmentName;

    @Column(name = "departmentType")
    private Integer departmentType = 1;

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
