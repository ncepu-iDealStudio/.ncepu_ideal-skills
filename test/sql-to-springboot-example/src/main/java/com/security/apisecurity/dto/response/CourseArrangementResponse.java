package com.security.apisecurity.dto.response;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CourseArrangementResponse {

    private Integer autoId;

    private String courseId;

    private String termId;

    private String classTime;

    private Integer count;

    private Boolean isDelete;

    private LocalDateTime addTime;
}
