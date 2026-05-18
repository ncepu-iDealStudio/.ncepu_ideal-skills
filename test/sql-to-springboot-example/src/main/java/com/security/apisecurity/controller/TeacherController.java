package com.security.apisecurity.controller;

import com.security.apisecurity.dto.request.TeacherRequest;
import com.security.apisecurity.dto.response.ApiResponse;
import com.security.apisecurity.dto.response.TeacherResponse;
import com.security.apisecurity.service.TeacherService;
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
@RequestMapping("/teachers")
@Tag(name = "Teacher Management", description = "Teacher management APIs")
@RequiredArgsConstructor
public class TeacherController {

    private final TeacherService teacherService;

    @PostMapping
    @Operation(summary = "Create new teacher", description = "Create a new teacher record")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "201",
            description = "Teacher created successfully",
            content = @Content(schema = @Schema(implementation = TeacherResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "400",
            description = "Invalid request data"
        )
    })
    public ResponseEntity<ApiResponse<TeacherResponse>> create(
            @Valid @RequestBody TeacherRequest request) {
        log.info("Creating new teacher");
        TeacherResponse response = teacherService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("Teacher created successfully", response));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get teacher by ID", description = "Get teacher information by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Teacher retrieved successfully",
            content = @Content(schema = @Schema(implementation = TeacherResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Teacher not found"
        )
    })
    public ResponseEntity<ApiResponse<TeacherResponse>> getById(
            @Parameter(description = "Teacher ID", required = true)
            @PathVariable Integer id) {
        log.debug("Getting teacher by id: {}", id);
        TeacherResponse response = teacherService.getById(id);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @GetMapping
    @Operation(summary = "Get teacher list", description = "Get paginated list of teacher")
    public ResponseEntity<ApiResponse<Page<TeacherResponse>>> getList(
            @Parameter(description = "Page number (0-based)", example = "0")
            @RequestParam(defaultValue = "0") int page,

            @Parameter(description = "Page size (1-100)", example = "20")
            @RequestParam(defaultValue = "20") int size,

            @Parameter(description = "Sort field", example = "addTime")
            @RequestParam(defaultValue = "addTime") String sortBy,

            @Parameter(description = "Sort direction", example = "desc")
            @RequestParam(defaultValue = "desc") String sortDir) {
        log.debug("Getting teacher list - page: {}, size: {}", page, size);
        Page<TeacherResponse> response = teacherService.getList(page, size, sortBy, sortDir);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update teacher", description = "Update teacher information")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Teacher updated successfully",
            content = @Content(schema = @Schema(implementation = TeacherResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Teacher not found"
        )
    })
    public ResponseEntity<ApiResponse<TeacherResponse>> update(
            @Parameter(description = "Teacher ID", required = true)
            @PathVariable Integer id,

            @Valid @RequestBody TeacherRequest request) {
        log.info("Updating teacher with id: {}", id);
        TeacherResponse response = teacherService.update(id, request);
        return ResponseEntity.ok(ApiResponse.success("Teacher updated successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete teacher", description = "Delete teacher by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Teacher deleted successfully"
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Teacher not found"
        )
    })
    public ResponseEntity<ApiResponse<Void>> delete(
            @Parameter(description = "Teacher ID", required = true)
            @PathVariable Integer id) {
        log.info("Deleting teacher with id: {}", id);
        teacherService.delete(id);
        return ResponseEntity.ok(ApiResponse.success("Teacher deleted successfully", null));
    }
}
