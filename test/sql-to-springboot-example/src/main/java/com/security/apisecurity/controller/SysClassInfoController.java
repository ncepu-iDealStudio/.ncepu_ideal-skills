package com.security.apisecurity.controller;

import com.security.apisecurity.dto.request.SysClassInfoRequest;
import com.security.apisecurity.dto.response.ApiResponse;
import com.security.apisecurity.dto.response.SysClassInfoResponse;
import com.security.apisecurity.service.SysClassInfoService;
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
@RequestMapping("/sys-classes")
@Tag(name = "SysClassInfo Management", description = "SysClassInfo management APIs")
@RequiredArgsConstructor
public class SysClassInfoController {

    private final SysClassInfoService sysClassInfoService;

    @PostMapping
    @Operation(summary = "Create new sys class info", description = "Create a new sys class info record")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "201",
            description = "Sys class info created successfully",
            content = @Content(schema = @Schema(implementation = SysClassInfoResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "400",
            description = "Invalid request data"
        )
    })
    public ResponseEntity<ApiResponse<SysClassInfoResponse>> create(
            @Valid @RequestBody SysClassInfoRequest request) {
        log.info("Creating new sys class info");
        SysClassInfoResponse response = sysClassInfoService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("Sys class info created successfully", response));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get sys class info by ID", description = "Get sys class info information by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Sys class info retrieved successfully",
            content = @Content(schema = @Schema(implementation = SysClassInfoResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Sys class info not found"
        )
    })
    public ResponseEntity<ApiResponse<SysClassInfoResponse>> getById(
            @Parameter(description = "Sys class info ID", required = true)
            @PathVariable Integer id) {
        log.debug("Getting sys class info by id: {}", id);
        SysClassInfoResponse response = sysClassInfoService.getById(id);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @GetMapping
    @Operation(summary = "Get sys class info list", description = "Get paginated list of sys class info")
    public ResponseEntity<ApiResponse<Page<SysClassInfoResponse>>> getList(
            @Parameter(description = "Page number (0-based)", example = "0")
            @RequestParam(defaultValue = "0") int page,

            @Parameter(description = "Page size (1-100)", example = "20")
            @RequestParam(defaultValue = "20") int size,

            @Parameter(description = "Sort field", example = "addTime")
            @RequestParam(defaultValue = "addTime") String sortBy,

            @Parameter(description = "Sort direction", example = "desc")
            @RequestParam(defaultValue = "desc") String sortDir) {
        log.debug("Getting sys class info list - page: {}, size: {}", page, size);
        Page<SysClassInfoResponse> response = sysClassInfoService.getList(page, size, sortBy, sortDir);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update sys class info", description = "Update sys class info information")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Sys class info updated successfully",
            content = @Content(schema = @Schema(implementation = SysClassInfoResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Sys class info not found"
        )
    })
    public ResponseEntity<ApiResponse<SysClassInfoResponse>> update(
            @Parameter(description = "Sys class info ID", required = true)
            @PathVariable Integer id,

            @Valid @RequestBody SysClassInfoRequest request) {
        log.info("Updating sys class info with id: {}", id);
        SysClassInfoResponse response = sysClassInfoService.update(id, request);
        return ResponseEntity.ok(ApiResponse.success("Sys class info updated successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete sys class info", description = "Delete sys class info by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Sys class info deleted successfully"
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Sys class info not found"
        )
    })
    public ResponseEntity<ApiResponse<Void>> delete(
            @Parameter(description = "Sys class info ID", required = true)
            @PathVariable Integer id) {
        log.info("Deleting sys class info with id: {}", id);
        sysClassInfoService.delete(id);
        return ResponseEntity.ok(ApiResponse.success("Sys class info deleted successfully", null));
    }
}
