package com.security.apisecurity.controller;

import com.security.apisecurity.dto.request.SysDepartmentInfoRequest;
import com.security.apisecurity.dto.response.ApiResponse;
import com.security.apisecurity.dto.response.SysDepartmentInfoResponse;
import com.security.apisecurity.service.SysDepartmentInfoService;
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
@RequestMapping("/sys-departments")
@Tag(name = "SysDepartmentInfo Management", description = "SysDepartmentInfo management APIs")
@RequiredArgsConstructor
public class SysDepartmentInfoController {

    private final SysDepartmentInfoService sysDepartmentInfoService;

    @PostMapping
    @Operation(summary = "Create new sys department info", description = "Create a new sys department info record")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "201",
            description = "Sys department info created successfully",
            content = @Content(schema = @Schema(implementation = SysDepartmentInfoResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "400",
            description = "Invalid request data"
        )
    })
    public ResponseEntity<ApiResponse<SysDepartmentInfoResponse>> create(
            @Valid @RequestBody SysDepartmentInfoRequest request) {
        log.info("Creating new sys department info");
        SysDepartmentInfoResponse response = sysDepartmentInfoService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("Sys department info created successfully", response));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get sys department info by ID", description = "Get sys department info information by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Sys department info retrieved successfully",
            content = @Content(schema = @Schema(implementation = SysDepartmentInfoResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Sys department info not found"
        )
    })
    public ResponseEntity<ApiResponse<SysDepartmentInfoResponse>> getById(
            @Parameter(description = "Sys department info ID", required = true)
            @PathVariable Long id) {
        log.debug("Getting sys department info by id: {}", id);
        SysDepartmentInfoResponse response = sysDepartmentInfoService.getById(id);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @GetMapping
    @Operation(summary = "Get sys department info list", description = "Get paginated list of sys department info")
    public ResponseEntity<ApiResponse<Page<SysDepartmentInfoResponse>>> getList(
            @Parameter(description = "Page number (0-based)", example = "0")
            @RequestParam(defaultValue = "0") int page,

            @Parameter(description = "Page size (1-100)", example = "20")
            @RequestParam(defaultValue = "20") int size,

            @Parameter(description = "Sort field", example = "addTime")
            @RequestParam(defaultValue = "addTime") String sortBy,

            @Parameter(description = "Sort direction", example = "desc")
            @RequestParam(defaultValue = "desc") String sortDir) {
        log.debug("Getting sys department info list - page: {}, size: {}", page, size);
        Page<SysDepartmentInfoResponse> response = sysDepartmentInfoService.getList(page, size, sortBy, sortDir);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update sys department info", description = "Update sys department info information")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Sys department info updated successfully",
            content = @Content(schema = @Schema(implementation = SysDepartmentInfoResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Sys department info not found"
        )
    })
    public ResponseEntity<ApiResponse<SysDepartmentInfoResponse>> update(
            @Parameter(description = "Sys department info ID", required = true)
            @PathVariable Long id,

            @Valid @RequestBody SysDepartmentInfoRequest request) {
        log.info("Updating sys department info with id: {}", id);
        SysDepartmentInfoResponse response = sysDepartmentInfoService.update(id, request);
        return ResponseEntity.ok(ApiResponse.success("Sys department info updated successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete sys department info", description = "Delete sys department info by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Sys department info deleted successfully"
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Sys department info not found"
        )
    })
    public ResponseEntity<ApiResponse<Void>> delete(
            @Parameter(description = "Sys department info ID", required = true)
            @PathVariable Long id) {
        log.info("Deleting sys department info with id: {}", id);
        sysDepartmentInfoService.delete(id);
        return ResponseEntity.ok(ApiResponse.success("Sys department info deleted successfully", null));
    }
}
