package com.security.apisecurity.dto.response;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class StudentResponse {

    private Integer autoId;

    private String studentId;

    private String userId;

    private String classId;

    private String collegeId;

    private String name;

    private String phoneNumber;

    private Integer age;

    private String agenda;

    private Boolean isDelete;

    private LocalDateTime addTime;
}
