package com.security.apisecurity.dto.response;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AdminResponse {

    private Integer autoId;

    private Long adminId;

    private String userId;

    private Long departmentId;

    private String name;

    private String email;

    private String phone;

    private String officeAddress;

    private Boolean isDelete;

    private LocalDateTime addTime;
}
