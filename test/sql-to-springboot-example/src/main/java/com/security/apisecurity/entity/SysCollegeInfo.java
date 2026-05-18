package com.security.apisecurity.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "sys_collegeInfo")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SysCollegeInfo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "autoID")
    private Long autoId;

    @Column(name = "collegeID", length = 20)
    private String collegeId;

    @Column(name = "collegeName", length = 50)
    private String collegeName;

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
