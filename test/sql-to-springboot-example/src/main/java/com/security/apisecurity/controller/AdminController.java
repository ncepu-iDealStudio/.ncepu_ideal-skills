package com.security.apisecurity.controller;

import com.security.apisecurity.dto.request.AdminRequest;
import com.security.apisecurity.dto.response.AdminResponse;
import com.security.apisecurity.dto.response.ApiResponse;
import com.security.apisecurity.service.AdminService;
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
@RequestMapping("/admins")
@Tag(name = "Admin Management", description = "Admin management APIs")
@RequiredArgsConstructor
public class AdminController {

    private final AdminService adminService;

    @PostMapping
    @Operation(summary = "Create new admin", description = "Create a new admin record")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "201",
            description = "Admin created successfully",
            content = @Content(schema = @Schema(implementation = AdminResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "400",
            description = "Invalid request data"
        )
    })
    public ResponseEntity<ApiResponse<AdminResponse>> create(
            @Valid @RequestBody AdminRequest request) {
        log.info("Creating new admin");
        AdminResponse response = adminService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("Admin created successfully", response));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get admin by ID", description = "Get admin information by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Admin retrieved successfully",
            content = @Content(schema = @Schema(implementation = AdminResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Admin not found"
        )
    })
    public ResponseEntity<ApiResponse<AdminResponse>> getById(
            @Parameter(description = "Admin ID", required = true)
            @PathVariable Integer id) {
        log.debug("Getting admin by id: {}", id);
        AdminResponse response = adminService.getById(id);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @GetMapping
    @Operation(summary = "Get admin list", description = "Get paginated list of admin")
    public ResponseEntity<ApiResponse<Page<AdminResponse>>> getList(
            @Parameter(description = "Page number (0-based)", example = "0")
            @RequestParam(defaultValue = "0") int page,

            @Parameter(description = "Page size (1-100)", example = "20")
            @RequestParam(defaultValue = "20") int size,

            @Parameter(description = "Sort field", example = "addTime")
            @RequestParam(defaultValue = "addTime") String sortBy,

            @Parameter(description = "Sort direction", example = "desc")
            @RequestParam(defaultValue = "desc") String sortDir) {
        log.debug("Getting admin list - page: {}, size: {}", page, size);
        Page<AdminResponse> response = adminService.getList(page, size, sortBy, sortDir);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update admin", description = "Update admin information")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Admin updated successfully",
            content = @Content(schema = @Schema(implementation = AdminResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Admin not found"
        )
    })
    public ResponseEntity<ApiResponse<AdminResponse>> update(
            @Parameter(description = "Admin ID", required = true)
            @PathVariable Integer id,

            @Valid @RequestBody AdminRequest request) {
        log.info("Updating admin with id: {}", id);
        AdminResponse response = adminService.update(id, request);
        return ResponseEntity.ok(ApiResponse.success("Admin updated successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete admin", description = "Delete admin by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Admin deleted successfully"
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Admin not found"
        )
    })
    public ResponseEntity<ApiResponse<Void>> delete(
            @Parameter(description = "Admin ID", required = true)
            @PathVariable Integer id) {
        log.info("Deleting admin with id: {}", id);
        adminService.delete(id);
        return ResponseEntity.ok(ApiResponse.success("Admin deleted successfully", null));
    }
}
