package com.security.apisecurity.controller;

import com.security.apisecurity.dto.request.StudentSelectedCourseRequest;
import com.security.apisecurity.dto.response.ApiResponse;
import com.security.apisecurity.dto.response.StudentSelectedCourseResponse;
import com.security.apisecurity.service.StudentSelectedCourseService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
@RequestMapping("/student-selected-courses")
@Tag(name = "StudentSelectedCourse Management", description = "StudentSelectedCourse management APIs")
@RequiredArgsConstructor
public class StudentSelectedCourseController {

    private final StudentSelectedCourseService studentSelectedCourseService;

    @PostMapping
    @Operation(summary = "Create new student selected course", description = "Create a new student selected course record")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "201",
            description = "Student selected course created successfully",
            content = @Content(schema = @Schema(implementation = StudentSelectedCourseResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "400",
            description = "Invalid request data"
        )
    })
    public ResponseEntity<ApiResponse<StudentSelectedCourseResponse>> create(
            @Valid @RequestBody StudentSelectedCourseRequest request) {
        log.info("Creating new student selected course");
        StudentSelectedCourseResponse response = studentSelectedCourseService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("Student selected course created successfully", response));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get student selected course by ID", description = "Get student selected course information by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Student selected course retrieved successfully",
            content = @Content(schema = @Schema(implementation = StudentSelectedCourseResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Student selected course not found"
        )
    })
    public ResponseEntity<ApiResponse<StudentSelectedCourseResponse>> getById(
            @Parameter(description = "Student selected course ID", required = true)
            @PathVariable Integer id) {
        log.debug("Getting student selected course by id: {}", id);
        StudentSelectedCourseResponse response = studentSelectedCourseService.getById(id);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @GetMapping
    @Operation(summary = "Get student selected course list", description = "Get paginated list of student selected course")
    public ResponseEntity<ApiResponse<Page<StudentSelectedCourseResponse>>> getList(
            @Parameter(description = "Page number (0-based)", example = "0")
            @RequestParam(defaultValue = "0") int page,

            @Parameter(description = "Page size (1-100)", example = "20")
            @RequestParam(defaultValue = "20") int size,

            @Parameter(description = "Sort field", example = "addTime")
            @RequestParam(defaultValue = "addTime") String sortBy,

            @Parameter(description = "Sort direction", example = "desc")
            @RequestParam(defaultValue = "desc") String sortDir) {
        log.debug("Getting student selected course list - page: {}, size: {}", page, size);
        Page<StudentSelectedCourseResponse> response = studentSelectedCourseService.getList(page, size, sortBy, sortDir);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update student selected course", description = "Update student selected course information")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Student selected course updated successfully",
            content = @Content(schema = @Schema(implementation = StudentSelectedCourseResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Student selected course not found"
        )
    })
    public ResponseEntity<ApiResponse<StudentSelectedCourseResponse>> update(
            @Parameter(description = "Student selected course ID", required = true)
            @PathVariable Integer id,

            @Valid @RequestBody StudentSelectedCourseRequest request) {
        log.info("Updating student selected course with id: {}", id);
        StudentSelectedCourseResponse response = studentSelectedCourseService.update(id, request);
        return ResponseEntity.ok(ApiResponse.success("Student selected course updated successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete student selected course", description = "Delete student selected course by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Student selected course deleted successfully"
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Student selected course not found"
        )
    })
    public ResponseEntity<ApiResponse<Void>> delete(
            @Parameter(description = "Student selected course ID", required = true)
            @PathVariable Integer id) {
        log.info("Deleting student selected course with id: {}", id);
        studentSelectedCourseService.delete(id);
        return ResponseEntity.ok(ApiResponse.success("Student selected course deleted successfully", null));
    }
}
