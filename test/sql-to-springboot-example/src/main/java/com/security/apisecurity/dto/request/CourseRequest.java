package com.security.apisecurity.dto.request;

import lombok.Data;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;

@Data
public class CourseRequest {

    @NotBlank(message = "课程编号不能为空")
    private String courseId;

    @NotBlank(message = "课程名称不能为空")
    private String courseName;

    private String teacherId;

    @Min(value = 0, message = "学分不能为负数")
    @Max(value = 10, message = "学分不能超过10")
    private Float credit;

    public CourseRequest() {
    }
}
