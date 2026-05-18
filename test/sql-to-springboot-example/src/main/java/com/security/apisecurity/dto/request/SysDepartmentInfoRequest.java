package com.security.apisecurity.dto.request;

import lombok.Data;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;

@Data
public class SysDepartmentInfoRequest {

    private Long departmentId;

    private Long parentDepartmentId;

    private String collegeId;

    private String departmentName;

    @Min(value = 1, message = "部门类型最小为1")
    @Max(value = 5, message = "部门类型最大为5")
    private Integer departmentType;

    public SysDepartmentInfoRequest() {
    }
}
