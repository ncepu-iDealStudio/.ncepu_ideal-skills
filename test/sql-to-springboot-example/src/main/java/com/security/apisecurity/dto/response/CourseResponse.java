package com.security.apisecurity.dto.response;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class CourseResponse {

    private Integer autoId;

    private String courseId;

    private String courseName;

    private String teacherId;

    private Float credit;

    private Boolean isDelete;

    private LocalDateTime addTime;
}
