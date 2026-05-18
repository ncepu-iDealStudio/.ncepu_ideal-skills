package com.security.apisecurity.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "sso_user")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class SsoUser {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "autoID")
    private Long autoId;

    @Column(name = "userID", length = 22)
    private String userId;

    @Column(name = "account", length = 255)
    private String account;

    @Column(name = "password", length = 255)
    private String password;

    @Column(name = "userType")
    private Integer userType;

    @Column(name = "status")
    private Integer status;

    @Column(name = "addTime")
    private LocalDateTime addTime;

    @PrePersist
    protected void onCreate() {
        if (addTime == null) {
            addTime = LocalDateTime.now();
        }
    }
}
