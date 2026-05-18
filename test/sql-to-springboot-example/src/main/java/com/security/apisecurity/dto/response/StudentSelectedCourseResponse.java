package com.security.apisecurity.dto.response;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class StudentSelectedCourseResponse {

    private Integer autoId;

    private String studentId;

    private String courseId;

    private Integer score;

    private Boolean isDelete;

    private LocalDateTime addTime;
}
