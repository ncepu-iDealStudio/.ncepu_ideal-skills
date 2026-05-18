package com.security.apisecurity.dto.response;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SysCollegeInfoResponse {

    private Long autoId;

    private String collegeId;

    private String collegeName;

    private Boolean isDelete;

    private LocalDateTime addTime;
}
