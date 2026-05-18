package com.security.apisecurity.controller;

import com.security.apisecurity.dto.request.{{className}}Request;
import com.security.apisecurity.dto.response.{{className}}Response;
import com.security.apisecurity.service.{{className}}Service;
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
@RequestMapping("/{{resourcePath}}")
@Tag(name = "{{className}} Management", description = "{{className}} management APIs")
@RequiredArgsConstructor
public class {{className}}Controller {

    private final {{className}}Service {{entityName}}Service;

    @PostMapping
    @Operation(summary = "Create new {{entityName}}", description = "Create a new {{entityName}} record")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "201",
            description = "{{className}} created successfully",
            content = @Content(schema = @Schema(implementation = {{className}}Response.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "400",
            description = "Invalid request data"
        )
    })
    public ResponseEntity<ApiResponse<{{className}}Response>> create(
            @Valid @RequestBody {{className}}Request request) {
        log.info("Creating new {{entityName}}");
        {{className}}Response response = {{entityName}}Service.create(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success("{{className}} created successfully", response));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get {{entityName}} by ID", description = "Get {{entityName}} information by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "{{className}} retrieved successfully",
            content = @Content(schema = @Schema(implementation = {{className}}Response.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "{{className}} not found"
        )
    })
    public ResponseEntity<ApiResponse<{{className}}Response>> getById(
            @Parameter(description = "{{className}} ID", required = true)
            @PathVariable {{pkType}} id) {
        log.debug("Getting {{entityName}} by id: {}", id);
        {{className}}Response response = {{entityName}}Service.getById(id);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @GetMapping
    @Operation(summary = "Get {{entityName}} list", description = "Get paginated list of {{entityName}}")
    public ResponseEntity<ApiResponse<Page<{{className}}Response>>> getList(
            @Parameter(description = "Page number (0-based)", example = "0")
            @RequestParam(defaultValue = "0") int page,

            @Parameter(description = "Page size (1-100)", example = "20")
            @RequestParam(defaultValue = "20") int size,

            @Parameter(description = "Sort field", example = "createTime")
            @RequestParam(defaultValue = "createTime") String sortBy,

            @Parameter(description = "Sort direction", example = "desc")
            @RequestParam(defaultValue = "desc") String sortDir{% if has模糊查询 %},

            @Parameter(description = "Search keyword")
            @RequestParam(required = false) String searchKeyword{% endif %}) {
        log.debug("Getting {{entityName}} list - page: {}, size: {}", page, size);
        Page<{{className}}Response> response = {{entityName}}Service.getList(page, size, sortBy, sortDir{% if has模糊查询 %}, searchKeyword{% endif %});
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @PutMapping("/{id}")
    @Operation(summary = "Update {{entityName}}", description = "Update {{entityName}} information")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "{{className}} updated successfully",
            content = @Content(schema = @Schema(implementation = {{className}}Response.class))
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "{{className}} not found"
        )
    })
    public ResponseEntity<ApiResponse<{{className}}Response>> update(
            @Parameter(description = "{{className}} ID", required = true)
            @PathVariable {{pkType}} id,

            @Valid @RequestBody {{className}}Request request) {
        log.info("Updating {{entityName}} with id: {}", id);
        {{className}}Response response = {{entityName}}Service.update(id, request);
        return ResponseEntity.ok(ApiResponse.success("{{className}} updated successfully", response));
    }

    @DeleteMapping("/{id}")
    @Operation(summary = "Delete {{entityName}}", description = "Delete {{entityName}} by ID")
    @ApiResponses(value = {
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "200",
            description = "{{className}} deleted successfully"
        ),
        @io.swagger.v3.oas.annotations.responses.ApiResponse(
            responseCode = "404",
            description = "{{className}} not found"
        )
    })
    public ResponseEntity<ApiResponse<Void>> delete(
            @Parameter(description = "{{className}} ID", required = true)
            @PathVariable {{pkType}} id) {
        log.info("Deleting {{entityName}} with id: {}", id);
        {{entityName}}Service.delete(id);
        return ResponseEntity.ok(ApiResponse.success("{{className}} deleted successfully", null));
    }
}
