package com.security.apisecurity.controller;

import com.security.apisecurity.dto.request.SysCollegeInfoRequest;
import com.security.apisecurity.dto.response.ApiResponse;
import com.security.apisecurity.dto.response.SysCollegeInfoResponse;
import com.security.apisecurity.service.SysCollegeInfoService;
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
@RequestMapping("/sys-colleges")
@Tag(name = "SysCollegeInfo Management", description = "SysCollegeInfo management APIs")
@RequiredArgsConstructor
public class SysCollegeInfoController {

    private final SysCollegeInfoService sysCollegeInfoService;

    @PostMapping
    @Operation(summary = "Create new sys college info", description = "Create a new sys college info record")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "201",
            description = "Sys college info created successfully",
            content = @Content(schema = @Schema(implementation = SysCollegeInfoResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "400",
            description = "Invalid request data"
        )
    })
    public ResponseEntity<ApiResponse<SysCollegeInfoResponse>> create(
            @Valid @RequestBody SysCollegeInfoRequest request) {
        log.info("Creating new sys college info");
        SysCollegeInfoResponse response = sysCollegeInfoService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("Sys college info created successfully", response));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get sys college info by ID", description = "Get sys college info information by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Sys college info retrieved successfully",
            content = @Content(schema = @Schema(implementation = SysCollegeInfoResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Sys college info not found"
        )
    })
    public ResponseEntity<ApiResponse<SysCollegeInfoResponse>> getById(
            @Parameter(description = "Sys college info ID", required = true)
            @PathVariable Long id) {
        log.debug("Getting sys college info by id: {}", id);
        SysCollegeInfoResponse response = sysCollegeInfoService.getById(id);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @GetMapping
    @Operation(summary = "Get sys college info list", description = "Get paginated list of sys college info")
    public ResponseEntity<ApiResponse<Page<SysCollegeInfoResponse>>> getList(
            @Parameter(description = "Page number (0-based)", example = "0")
            @RequestParam(defaultValue = "0") int page,

            @Parameter(description = "Page size (1-100)", example = "20")
            @RequestParam(defaultValue = "20") int size,

            @Parameter(description = "Sort field", example = "addTime")
            @RequestParam(defaultValue = "addTime") String sortBy,

            @Parameter(description = "Sort direction", example = "desc")
            @RequestParam(defaultValue = "desc") String sortDir) {
        log.debug("Getting sys college info list - page: {}, size: {}", page, size);
        Page<SysCollegeInfoResponse> response = sysCollegeInfoService.getList(page, size, sortBy, sortDir);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update sys college info", description = "Update sys college info information")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Sys college info updated successfully",
            content = @Content(schema = @Schema(implementation = SysCollegeInfoResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Sys college info not found"
        )
    })
    public ResponseEntity<ApiResponse<SysCollegeInfoResponse>> update(
            @Parameter(description = "Sys college info ID", required = true)
            @PathVariable Long id,

            @Valid @RequestBody SysCollegeInfoRequest request) {
        log.info("Updating sys college info with id: {}", id);
        SysCollegeInfoResponse response = sysCollegeInfoService.update(id, request);
        return ResponseEntity.ok(ApiResponse.success("Sys college info updated successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete sys college info", description = "Delete sys college info by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Sys college info deleted successfully"
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Sys college info not found"
        )
    })
    public ResponseEntity<ApiResponse<Void>> delete(
            @Parameter(description = "Sys college info ID", required = true)
            @PathVariable Long id) {
        log.info("Deleting sys college info with id: {}", id);
        sysCollegeInfoService.delete(id);
        return ResponseEntity.ok(ApiResponse.success("Sys college info deleted successfully", null));
    }
}
