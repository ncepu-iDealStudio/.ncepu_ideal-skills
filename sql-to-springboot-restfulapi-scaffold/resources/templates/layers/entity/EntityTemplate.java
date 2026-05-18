package com.security.apisecurity.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
{% for import in additional_imports %}
{{ import }}
{% endfor %}

@Entity
@Table(name = "{{table_name}}")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class {{className}} {

{% for field in fields %}
    {% if field.comment %}
    {{field.comment}}
    {% endif %}
    {% if field.validation_annotation %}
    {{field.validation_annotation}}
    {% endif %}
    @Column(name = "{{field.db_column_name}}"{% if field.type %}, columnDefinition = "{{field.type}}"{% endif %}{% if field.nullable == false %}, nullable = false{% endif %}{% if field.unique %}, unique = true{% endif %}{% if field.comment %}, columnDefinition = "{{field.comment}}"{% endif %})
    private{{field.javaType}} {{field.fieldName}}{% if field.defaultValue %} = {{field.defaultValue}}{% endif %};

{% endfor %}
{% for relation in relations %}
    {% if relation.type == "ManyToOne" %}
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "{{relation.columnName}}", referencedColumnName = "{{relation.referencedColumnName}}", insertable = false, updatable = false)
    private {{relation.targetClass}} {{relation.propertyName}};

    {% elif relation.type == "OneToOne" %}
    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "{{relation.columnName}}", referencedColumnName = "{{relation.referencedColumnName}}", insertable = false, updatable = false)
    private {{relation.targetClass}} {{relation.propertyName}};

    {% elif relation.type == "OneToMany" %}
    @OneToMany(mappedBy = "{{relation.mappedBy}}", fetch = FetchType.LAZY)
    private List<{{relation.targetClass}}> {{relation.propertyName}};

    {% endif %}
{% endfor %}
{% if has_prepersist %}
    @PrePersist
    protected void onCreate() {
        if (createTime == null) {
            createTime = LocalDateTime.now();
        }
    }
{% endif %}
}
