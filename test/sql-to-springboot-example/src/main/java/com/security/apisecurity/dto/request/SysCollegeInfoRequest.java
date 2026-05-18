package com.security.apisecurity.dto.request;

import lombok.Data;
import jakarta.validation.constraints.NotBlank;

@Data
public class SysCollegeInfoRequest {

    @NotBlank(message = "学院ID不能为空")
    private String collegeId;

    @NotBlank(message = "学院名称不能为空")
    private String collegeName;

    public SysCollegeInfoRequest() {
    }
}
