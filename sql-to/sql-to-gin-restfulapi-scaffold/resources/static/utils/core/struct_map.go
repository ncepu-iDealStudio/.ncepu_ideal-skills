package core

import (
	"fmt"
	"reflect"
)

// StructToTaggedMap converts a struct (or struct pointer) into map by tag name.
// When omitZero is true, zero-value fields are skipped.
func StructToTaggedMap(in any, tagName string, omitZero bool) (map[string]any, error) {
	v := reflect.ValueOf(in)
	if v.Kind() == reflect.Ptr {
		if v.IsNil() {
			return nil, fmt.Errorf("nil pointer input")
		}
		v = v.Elem()
	}
	if v.Kind() != reflect.Struct {
		return nil, fmt.Errorf("only accepts struct or struct pointer; got %T", in)
	}

	t := v.Type()
	out := make(map[string]any)
	for i := 0; i < v.NumField(); i++ {
		field := v.Field(i)
		if !field.IsValid() {
			continue
		}
		if omitZero && field.IsZero() {
			continue
		}
		tag := t.Field(i).Tag.Get(tagName)
		if tag == "" || tag == "-" {
			continue
		}
		out[tag] = field.Interface()
	}
	return out, nil
}

// AssignByTag assigns fields from src to dst by matching tag values.
// dst and src must be struct pointers.
func AssignByTag(dst any, src any, tagName string, ignoreZero bool) error {
	dv := reflect.ValueOf(dst)
	sv := reflect.ValueOf(src)

	if dv.Kind() != reflect.Ptr || dv.IsNil() {
		return fmt.Errorf("dst must be non-nil pointer")
	}
	if sv.Kind() != reflect.Ptr || sv.IsNil() {
		return fmt.Errorf("src must be non-nil pointer")
	}

	dv = dv.Elem()
	sv = sv.Elem()
	if dv.Kind() != reflect.Struct || sv.Kind() != reflect.Struct {
		return fmt.Errorf("dst and src must point to structs")
	}

	dt := dv.Type()
	st := sv.Type()

	tagIndex := map[string]int{}
	for i := 0; i < dt.NumField(); i++ {
		tag := dt.Field(i).Tag.Get(tagName)
		if tag != "" && tag != "-" {
			tagIndex[tag] = i
		}
	}

	for i := 0; i < sv.NumField(); i++ {
		sField := sv.Field(i)
		if !sField.IsValid() {
			continue
		}
		if ignoreZero && sField.IsZero() {
			continue
		}

		tag := st.Field(i).Tag.Get(tagName)
		j, ok := tagIndex[tag]
		if !ok {
			continue
		}

		dField := dv.Field(j)
		if !dField.CanSet() {
			continue
		}
		if sField.Type().AssignableTo(dField.Type()) {
			dField.Set(sField)
			continue
		}
		if sField.Type().ConvertibleTo(dField.Type()) {
			dField.Set(sField.Convert(dField.Type()))
		}
	}
	return nil
}
