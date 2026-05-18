package com.security.apisecurity.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "admin")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Admin {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "auto_id")
    private Integer autoId;

    @Column(name = "admin_id", columnDefinition = "bigint")
    private Long adminId;

    @Column(name = "user_id", length = 22)
    private String userId;

    @Column(name = "department_id", columnDefinition = "bigint")
    private Long departmentId;

    @Column(name = "name", length = 10)
    private String name;

    @Column(name = "email", length = 50)
    private String email;

    @Column(name = "phone", length = 100)
    private String phone;

    @Column(name = "office_address", length = 255)
    private String officeAddress;

    @Column(name = "is_delete")
    private Boolean isDelete = false;

    @Column(name = "add_time")
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
