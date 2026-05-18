package com.security.apisecurity.service;

import com.security.apisecurity.dto.request.{{className}}Request;
import com.security.apisecurity.dto.response.{{className}}Response;
import com.security.apisecurity.entity.{{className}};
import com.security.apisecurity.exception.ResourceNotFoundException;
import com.security.apisecurity.repository.{{className}}Repository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@Transactional
@RequiredArgsConstructor
public class {{className}}Service {

    private final {{className}}Repository {{entityName}}Repository;

    public {{className}}Response create({{className}}Request request) {
        {{className}} entity = new {{className}}();
        {# ===== 创建时设置所有请求字段 ===== #}
        {% for field in requestFields %}
        entity.set{{field.methodSuffix}}(request.get{{field.methodSuffix}}());
        {% endfor %}

        {{className}} saved = {{entityName}}Repository.save(entity);
        log.info("Created {{entityName}} with id: {}", saved.get{{pkMethodSuffix}}());

        return mapToResponse(saved);
    }

    public {{className}}Response getById({{pkType}} id) {
        {{className}} entity = findEntityById(id);
        return mapToResponse(entity);
    }

    public Page<{{className}}Response> getList(int page, int size, String sortBy, String sortDir{% if has模糊查询 %}, String searchKeyword{% endif %}) {
        Sort sort = Sort.by(Sort.Direction.fromString(sortDir), sortBy);
        Pageable pageable = PageRequest.of(page, size, sort);

        Page<{{className}}> entities;
        {% if has软删除 %}
        {% if has模糊查询 %}
        if (searchKeyword != null && !searchKeyword.trim().isEmpty()) {
            entities = {{entityName}}Repository.findBy{{queryFieldMethodName}}ContainingAnd{{softDeleteFieldUpper}}(searchKeyword.trim(), pageable);
        } else {
            entities = {{entityName}}Repository.findBy{{softDeleteFieldUpper}}(false, pageable);
        }
        {% else %}
        entities = {{entityName}}Repository.findBy{{softDeleteFieldUpper}}(false, pageable);
        {% endif %}
        {% else %}
        entities = {{entityName}}Repository.findAll(pageable);
        {% endif %}

        return entities.map(this::mapToResponse);
    }

    public {{className}}Response update({{pkType}} id, {{className}}Request request) {
        {{className}} entity = findEntityById(id);
        {# ===== 更新时检查非空，只更新有值的字段 ===== #}
        {% for field in requestFields %}
        {% if field.nullable %}
        if (request.get{{field.methodSuffix}}() != null) {
            entity.set{{field.methodSuffix}}(request.get{{field.methodSuffix}}());
        }
        {% else %}
        entity.set{{field.methodSuffix}}(request.get{{field.methodSuffix}}());
        {% endif %}
        {% endfor %}

        {{className}} updated = {{entityName}}Repository.save(entity);
        log.info("Updated {{entityName}} with id: {}", updated.get{{pkMethodSuffix}}());

        return mapToResponse(updated);
    }

    public void delete({{pkType}} id) {
        {{className}} entity = findEntityById(id);
        {% if has软删除 %}
        entity.set{{softDeleteMethodSuffix}}(true);
        {{entityName}}Repository.save(entity);
        log.info("Soft deleted {{entityName}} with id: {}", id);
        {% else %}
        {{entityName}}Repository.delete(entity);
        log.info("Hard deleted {{entityName}} with id: {}", id);
        {% endif %}
    }

    private {{className}} findEntityById({{pkType}} id) {
        {% if has软删除 %}
        return {{entityName}}Repository.findBy{{pkMethodSuffix}}And{{softDeleteFieldUpper}}(id, false)
                .orElseThrow(() -> new ResourceNotFoundException("{{className}} not found with id: " + id));
        {% else %}
        return {{entityName}}Repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("{{className}} not found with id: " + id));
        {% endif %}
    }

    private {{className}}Response mapToResponse({{className}} entity) {
        {% if has关联查询 %}
        String relatedName = null;
        {% for relation in relations %}
        {% if relation.type == "ManyToOne" %}
        if (entity.get{{relation.methodSuffix}}() != null) {
            relatedName = entity.get{{relation.methodSuffix}}().get{{relation.displayField}}();
        }
        {% endif %}
        {% endfor %}
        {% endif %}
        return new {{className}}Response(
                {% for field in responseFields %}
                entity.get{{field.methodSuffix}}(){% if not loop.last %},{% endif %}
                {% endfor %}
        );
    }
}
