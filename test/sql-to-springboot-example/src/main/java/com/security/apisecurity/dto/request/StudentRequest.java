package com.security.apisecurity.dto.request;

import lombok.Data;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Pattern;

@Data
public class StudentRequest {

    @NotBlank(message = "学号不能为空")
    private String studentId;

    private String userId;

    private String classId;

    private String collegeId;

    @NotBlank(message = "姓名不能为空")
    private String name;

    @Pattern(regexp = "^[1][3-9]\\d{9}$", message = "手机号格式不正确")
    private String phoneNumber;

    @Min(value = 0, message = "年龄不能小于0")
    @Max(value = 150, message = "年龄不能大于150")
    private Integer age;

    @Pattern(regexp = "^[男女其他]$", message = "性别只能是：男、女、其他")
    private String agenda;

    public StudentRequest() {
    }
}
