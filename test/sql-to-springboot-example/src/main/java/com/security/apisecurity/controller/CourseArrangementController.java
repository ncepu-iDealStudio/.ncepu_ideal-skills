package com.security.apisecurity.controller;

import com.security.apisecurity.dto.request.CourseArrangementRequest;
import com.security.apisecurity.dto.response.ApiResponse;
import com.security.apisecurity.dto.response.CourseArrangementResponse;
import com.security.apisecurity.service.CourseArrangementService;
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
@RequestMapping("/course-arrangements")
@Tag(name = "CourseArrangement Management", description = "CourseArrangement management APIs")
@RequiredArgsConstructor
public class CourseArrangementController {

    private final CourseArrangementService courseArrangementService;

    @PostMapping
    @Operation(summary = "Create new course arrangement", description = "Create a new course arrangement record")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "201",
            description = "Course arrangement created successfully",
            content = @Content(schema = @Schema(implementation = CourseArrangementResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "400",
            description = "Invalid request data"
        )
    })
    public ResponseEntity<ApiResponse<CourseArrangementResponse>> create(
            @Valid @RequestBody CourseArrangementRequest request) {
        log.info("Creating new course arrangement");
        CourseArrangementResponse response = courseArrangementService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("Course arrangement created successfully", response));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get course arrangement by ID", description = "Get course arrangement information by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Course arrangement retrieved successfully",
            content = @Content(schema = @Schema(implementation = CourseArrangementResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Course arrangement not found"
        )
    })
    public ResponseEntity<ApiResponse<CourseArrangementResponse>> getById(
            @Parameter(description = "Course arrangement ID", required = true)
            @PathVariable Integer id) {
        log.debug("Getting course arrangement by id: {}", id);
        CourseArrangementResponse response = courseArrangementService.getById(id);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @GetMapping
    @Operation(summary = "Get course arrangement list", description = "Get paginated list of course arrangement")
    public ResponseEntity<ApiResponse<Page<CourseArrangementResponse>>> getList(
            @Parameter(description = "Page number (0-based)", example = "0")
            @RequestParam(defaultValue = "0") int page,

            @Parameter(description = "Page size (1-100)", example = "20")
            @RequestParam(defaultValue = "20") int size,

            @Parameter(description = "Sort field", example = "addTime")
            @RequestParam(defaultValue = "addTime") String sortBy,

            @Parameter(description = "Sort direction", example = "desc")
            @RequestParam(defaultValue = "desc") String sortDir) {
        log.debug("Getting course arrangement list - page: {}, size: {}", page, size);
        Page<CourseArrangementResponse> response = courseArrangementService.getList(page, size, sortBy, sortDir);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update course arrangement", description = "Update course arrangement information")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Course arrangement updated successfully",
            content = @Content(schema = @Schema(implementation = CourseArrangementResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Course arrangement not found"
        )
    })
    public ResponseEntity<ApiResponse<CourseArrangementResponse>> update(
            @Parameter(description = "Course arrangement ID", required = true)
            @PathVariable Integer id,

            @Valid @RequestBody CourseArrangementRequest request) {
        log.info("Updating course arrangement with id: {}", id);
        CourseArrangementResponse response = courseArrangementService.update(id, request);
        return ResponseEntity.ok(ApiResponse.success("Course arrangement updated successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete course arrangement", description = "Delete course arrangement by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Course arrangement deleted successfully"
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Course arrangement not found"
        )
    })
    public ResponseEntity<ApiResponse<Void>> delete(
            @Parameter(description = "Course arrangement ID", required = true)
            @PathVariable Integer id) {
        log.info("Deleting course arrangement with id: {}", id);
        courseArrangementService.delete(id);
        return ResponseEntity.ok(ApiResponse.success("Course arrangement deleted successfully", null));
    }
}
