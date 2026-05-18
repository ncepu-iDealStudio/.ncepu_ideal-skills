package com.security.apisecurity.dto.request;

import lombok.Data;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Pattern;

@Data
public class AdminRequest {

    private Long adminId;

    private String userId;

    private Long departmentId;

    private String name;

    @Email(message = "邮箱格式不正确")
    private String email;

    @Pattern(regexp = "^[1][3-9]\\d{9}$", message = "手机号格式不正确")
    private String phone;

    private String officeAddress;

    public AdminRequest() {
    }
}
