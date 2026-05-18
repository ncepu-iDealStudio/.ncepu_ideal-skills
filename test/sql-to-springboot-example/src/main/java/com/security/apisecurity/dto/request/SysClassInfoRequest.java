package com.security.apisecurity.dto.request;

import lombok.Data;
import jakarta.validation.constraints.NotBlank;

@Data
public class SysClassInfoRequest {

    @NotBlank(message = "班级ID不能为空")
    private String classId;

    private String collegeId;

    private String className;

    public SysClassInfoRequest() {
    }
}
