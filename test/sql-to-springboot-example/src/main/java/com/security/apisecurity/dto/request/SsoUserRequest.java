package com.security.apisecurity.dto.request;

import lombok.Data;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;

@Data
public class SsoUserRequest {

    @NotBlank(message = "用户ID不能为空")
    private String userId;

    @NotBlank(message = "账号不能为空")
    private String account;

    private String password;

    @Min(value = 1, message = "账号类型最小为1")
    @Max(value = 3, message = "账号类型最大为3")
    private Integer userType;

    @Min(value = 0, message = "状态值最小为0")
    @Max(value = 1, message = "状态值最大为1")
    private Integer status;

    public SsoUserRequest() {
    }
}
