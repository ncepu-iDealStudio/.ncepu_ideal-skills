package com.security.apisecurity.dto.response;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SysClassInfoResponse {

    private Integer autoId;

    private String classId;

    private String collegeId;

    private String className;

    private Boolean isDeleted;

    private LocalDateTime addTime;
}
