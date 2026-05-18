package com.security.apisecurity.dto.response;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SysDepartmentInfoResponse {

    private Long autoId;

    private Long departmentId;

    private Long parentDepartmentId;

    private String collegeId;

    private String departmentName;

    private Integer departmentType;

    private Boolean isDeleted;

    private LocalDateTime addTime;
}
