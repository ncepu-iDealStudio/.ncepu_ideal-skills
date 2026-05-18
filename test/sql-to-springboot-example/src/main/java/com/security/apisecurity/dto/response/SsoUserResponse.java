package com.security.apisecurity.dto.response;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SsoUserResponse {

    private Long autoId;

    private String userId;

    private String account;

    private Integer userType;

    private Integer status;

    private LocalDateTime addTime;
}
