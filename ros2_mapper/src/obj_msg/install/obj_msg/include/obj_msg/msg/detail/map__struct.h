// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from obj_msg:msg/Map.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__MAP__STRUCT_H_
#define OBJ_MSG__MSG__DETAIL__MAP__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'm'
#include "obj_msg/msg/detail/map_info__struct.h"
// Member 'objects'
#include "obj_msg/msg/detail/obj__struct.h"

// Struct defined in msg/Map in the package obj_msg.
typedef struct obj_msg__msg__Map
{
  obj_msg__msg__MapInfo m;
  obj_msg__msg__Obj__Sequence objects;
} obj_msg__msg__Map;

// Struct for a sequence of obj_msg__msg__Map.
typedef struct obj_msg__msg__Map__Sequence
{
  obj_msg__msg__Map * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} obj_msg__msg__Map__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // OBJ_MSG__MSG__DETAIL__MAP__STRUCT_H_
