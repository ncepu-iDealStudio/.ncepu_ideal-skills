package com.security.apisecurity.dto.request;

import lombok.Data;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;

@Data
public class StudentSelectedCourseRequest {

    @NotBlank(message = "学号不能为空")
    private String studentId;

    @NotBlank(message = "课程编号不能为空")
    private String courseId;

    @Min(value = 0, message = "成绩不能为负数")
    @Max(value = 100, message = "成绩不能超过100")
    private Integer score;

    public StudentSelectedCourseRequest() {
    }
}
