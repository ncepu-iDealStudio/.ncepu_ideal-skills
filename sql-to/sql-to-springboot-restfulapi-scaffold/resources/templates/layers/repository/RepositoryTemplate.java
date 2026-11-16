/**
 * 【AUTO-GENERATED】由 sql-to-springboot-scaffold 生成；表结构变更时技能会重生成。
 * 注意：派生查询方法名由软删字段名与主键名拼出，字段变化必须整体重生成，
 * 否则 Spring Data JPA 启动期抛 No property ... found。
 */
package com.security.apisecurity.repository;

import com.security.apisecurity.entity.{{className}};
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

{% if has软删除 %}
import java.util.List;
import java.util.Optional;
{% else %}
import java.util.Optional;
{% endif %}

@Repository
public interface {{className}}Repository extends JpaRepository<{{className}}, {{pkType}}> {

{% if has软删除 %}
    Optional<{{className}}> findBy{{pkPropertyNameUpper}}And{{softDeleteFieldUpper}}({{pkType}} {{pkPropertyName}});

    Page<{{className}}> findBy{{softDeleteFieldUpper}}(boolean {{softDeleteField}}, Pageable pageable);

    List<{{className}}> findBy{{softDeleteFieldUpper}}(boolean {{softDeleteField}});
{% endif %}
{% for fk in foreignKeys %}

    Page<{{className}}> findBy{{fk.propertyNameUpper}}And{{softDeleteFieldUpper}}({{fk.type}} {{fk.propertyName}}, boolean {{softDeleteField}}, Pageable pageable);

    List<{{className}}> findBy{{fk.propertyNameUpper}}And{{softDeleteFieldUpper}}({{fk.type}} {{fk.propertyName}}, boolean {{softDeleteField}});
{% endfor %}
{% if has模糊查询 %}

    @Query("SELECT e FROM {{className}} e WHERE e.{{queryField}} LIKE %:{{queryParam}}% AND e.{{softDeleteField}} = false")
    Page<{{className}}> findBy{{queryFieldMethodName}}ContainingAnd{{softDeleteFieldUpper}}(@Param("{{queryParam}}") String {{queryParam}}, Pageable pageable);
{% endif %}
}
