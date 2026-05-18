package com.security.apisecurity.controller;

import com.security.apisecurity.dto.request.StudentRequest;
import com.security.apisecurity.dto.response.ApiResponse;
import com.security.apisecurity.dto.response.StudentResponse;
import com.security.apisecurity.service.StudentService;
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
@RequestMapping("/students")
@Tag(name = "Student Management", description = "Student management APIs")
@RequiredArgsConstructor
public class StudentController {

    private final StudentService studentService;

    @PostMapping
    @Operation(summary = "Create new student", description = "Create a new student record")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "201",
            description = "Student created successfully",
            content = @Content(schema = @Schema(implementation = StudentResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "400",
            description = "Invalid request data"
        )
    })
    public ResponseEntity<ApiResponse<StudentResponse>> create(
            @Valid @RequestBody StudentRequest request) {
        log.info("Creating new student");
        StudentResponse response = studentService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("Student created successfully", response));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get student by ID", description = "Get student information by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Student retrieved successfully",
            content = @Content(schema = @Schema(implementation = StudentResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Student not found"
        )
    })
    public ResponseEntity<ApiResponse<StudentResponse>> getById(
            @Parameter(description = "Student ID", required = true)
            @PathVariable Integer id) {
        log.debug("Getting student by id: {}", id);
        StudentResponse response = studentService.getById(id);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @GetMapping
    @Operation(summary = "Get student list", description = "Get paginated list of student")
    public ResponseEntity<ApiResponse<Page<StudentResponse>>> getList(
            @Parameter(description = "Page number (0-based)", example = "0")
            @RequestParam(defaultValue = "0") int page,

            @Parameter(description = "Page size (1-100)", example = "20")
            @RequestParam(defaultValue = "20") int size,

            @Parameter(description = "Sort field", example = "addTime")
            @RequestParam(defaultValue = "addTime") String sortBy,

            @Parameter(description = "Sort direction", example = "desc")
            @RequestParam(defaultValue = "desc") String sortDir) {
        log.debug("Getting student list - page: {}, size: {}", page, size);
        Page<StudentResponse> response = studentService.getList(page, size, sortBy, sortDir);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update student", description = "Update student information")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Student updated successfully",
            content = @Content(schema = @Schema(implementation = StudentResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Student not found"
        )
    })
    public ResponseEntity<ApiResponse<StudentResponse>> update(
            @Parameter(description = "Student ID", required = true)
            @PathVariable Integer id,

            @Valid @RequestBody StudentRequest request) {
        log.info("Updating student with id: {}", id);
        StudentResponse response = studentService.update(id, request);
        return ResponseEntity.ok(ApiResponse.success("Student updated successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete student", description = "Delete student by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Student deleted successfully"
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Student not found"
        )
    })
    public ResponseEntity<ApiResponse<Void>> delete(
            @Parameter(description = "Student ID", required = true)
            @PathVariable Integer id) {
        log.info("Deleting student with id: {}", id);
        studentService.delete(id);
        return ResponseEntity.ok(ApiResponse.success("Student deleted successfully", null));
    }
}
