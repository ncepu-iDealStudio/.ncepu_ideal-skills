package com.security.apisecurity.dto.request;

import lombok.Data;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;

@Data
public class CourseArrangementRequest {

    @NotBlank(message = "课程编号不能为空")
    private String courseId;

    private String termId;

    private String classTime;

    @Min(value = 0, message = "课程容量不能为负数")
    @Max(value = 500, message = "课程容量不能超过500")
    private Integer count;

    public CourseArrangementRequest() {
    }
}
