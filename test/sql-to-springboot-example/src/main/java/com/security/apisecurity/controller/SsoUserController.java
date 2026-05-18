package com.security.apisecurity.controller;

import com.security.apisecurity.dto.request.SsoUserRequest;
import com.security.apisecurity.dto.response.ApiResponse;
import com.security.apisecurity.dto.response.SsoUserResponse;
import com.security.apisecurity.service.SsoUserService;
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
@RequestMapping("/sso-users")
@Tag(name = "SsoUser Management", description = "SsoUser management APIs")
@RequiredArgsConstructor
public class SsoUserController {

    private final SsoUserService ssoUserService;

    @PostMapping
    @Operation(summary = "Create new sso user", description = "Create a new sso user record")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "201",
            description = "Sso user created successfully",
            content = @Content(schema = @Schema(implementation = SsoUserResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "400",
            description = "Invalid request data"
        )
    })
    public ResponseEntity<ApiResponse<SsoUserResponse>> create(
            @Valid @RequestBody SsoUserRequest request) {
        log.info("Creating new sso user");
        SsoUserResponse response = ssoUserService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("Sso user created successfully", response));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get sso user by ID", description = "Get sso user information by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Sso user retrieved successfully",
            content = @Content(schema = @Schema(implementation = SsoUserResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Sso user not found"
        )
    })
    public ResponseEntity<ApiResponse<SsoUserResponse>> getById(
            @Parameter(description = "Sso user ID", required = true)
            @PathVariable Long id) {
        log.debug("Getting sso user by id: {}", id);
        SsoUserResponse response = ssoUserService.getById(id);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @GetMapping
    @Operation(summary = "Get sso user list", description = "Get paginated list of sso user")
    public ResponseEntity<ApiResponse<Page<SsoUserResponse>>> getList(
            @Parameter(description = "Page number (0-based)", example = "0")
            @RequestParam(defaultValue = "0") int page,

            @Parameter(description = "Page size (1-100)", example = "20")
            @RequestParam(defaultValue = "20") int size,

            @Parameter(description = "Sort field", example = "addTime")
            @RequestParam(defaultValue = "addTime") String sortBy,

            @Parameter(description = "Sort direction", example = "desc")
            @RequestParam(defaultValue = "desc") String sortDir) {
        log.debug("Getting sso user list - page: {}, size: {}", page, size);
        Page<SsoUserResponse> response = ssoUserService.getList(page, size, sortBy, sortDir);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update sso user", description = "Update sso user information")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Sso user updated successfully",
            content = @Content(schema = @Schema(implementation = SsoUserResponse.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Sso user not found"
        )
    })
    public ResponseEntity<ApiResponse<SsoUserResponse>> update(
            @Parameter(description = "Sso user ID", required = true)
            @PathVariable Long id,

            @Valid @RequestBody SsoUserRequest request) {
        log.info("Updating sso user with id: {}", id);
        SsoUserResponse response = ssoUserService.update(id, request);
        return ResponseEntity.ok(ApiResponse.success("Sso user updated successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete sso user", description = "Delete sso user by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "Sso user deleted successfully"
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "Sso user not found"
        )
    })
    public ResponseEntity<ApiResponse<Void>> delete(
            @Parameter(description = "Sso user ID", required = true)
            @PathVariable Long id) {
        log.info("Deleting sso user with id: {}", id);
        ssoUserService.delete(id);
        return ResponseEntity.ok(ApiResponse.success("Sso user deleted successfully", null));
    }
}
