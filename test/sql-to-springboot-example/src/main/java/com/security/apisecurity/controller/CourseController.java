package com.security.apisecurity.controller;

import com.security.apisecurity.dto.request.CourseRequest;
import com.security.apisecurity.dto.response.ApiResponse;
import com.security.apisecurity.dto.response.CourseResponse;
import com.security.apisecurity.service.CourseService;
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
@RequestMapping("/courses")
@Tag(name = "Course Management", description = "Course management APIs")
@RequiredArgsConstructor
public class CourseController {

    private final CourseService courseService;

    @PostMapping
    @Operation(summary = "Create new course", description = "Create a new course record")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "201",
            description = "Course created successfully",
            content = @Content(schema = @Schema(implementation = CourseResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "400",
            description = "Invalid request data"
        )
    })
    public ResponseEntity<ApiResponse<CourseResponse>> create(
            @Valid @RequestBody CourseRequest request) {
        log.info("Creating new course");
        CourseResponse response = courseService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("Course created successfully", response));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get course by ID", description = "Get course information by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Course retrieved successfully",
            content = @Content(schema = @Schema(implementation = CourseResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Course not found"
        )
    })
    public ResponseEntity<ApiResponse<CourseResponse>> getById(
            @Parameter(description = "Course ID", required = true)
            @PathVariable Integer id) {
        log.debug("Getting course by id: {}", id);
        CourseResponse response = courseService.getById(id);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @GetMapping
    @Operation(summary = "Get course list", description = "Get paginated list of course")
    public ResponseEntity<ApiResponse<Page<CourseResponse>>> getList(
            @Parameter(description = "Page number (0-based)", example = "0")
            @RequestParam(defaultValue = "0") int page,

            @Parameter(description = "Page size (1-100)", example = "20")
            @RequestParam(defaultValue = "20") int size,

            @Parameter(description = "Sort field", example = "addTime")
            @RequestParam(defaultValue = "addTime") String sortBy,

            @Parameter(description = "Sort direction", example = "desc")
            @RequestParam(defaultValue = "desc") String sortDir) {
        log.debug("Getting course list - page: {}, size: {}", page, size);
        Page<CourseResponse> response = courseService.getList(page, size, sortBy, sortDir);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update course", description = "Update course information")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Course updated successfully",
            content = @Content(schema = @Schema(implementation = CourseResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Course not found"
        )
    })
    public ResponseEntity<ApiResponse<CourseResponse>> update(
            @Parameter(description = "Course ID", required = true)
            @PathVariable Integer id,

            @Valid @RequestBody CourseRequest request) {
        log.info("Updating course with id: {}", id);
        CourseResponse response = courseService.update(id, request);
        return ResponseEntity.ok(ApiResponse.success("Course updated successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete course", description = "Delete course by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Course deleted successfully"
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Course not found"
        )
    })
    public ResponseEntity<ApiResponse<Void>> delete(
            @Parameter(description = "Course ID", required = true)
            @PathVariable Integer id) {
        log.info("Deleting course with id: {}", id);
        courseService.delete(id);
        return ResponseEntity.ok(ApiResponse.success("Course deleted successfully", null));
    }
}
