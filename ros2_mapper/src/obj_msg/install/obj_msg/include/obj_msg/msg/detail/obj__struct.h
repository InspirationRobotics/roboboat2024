// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from obj_msg:msg/Obj.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__OBJ__STRUCT_H_
#define OBJ_MSG__MSG__DETAIL__OBJ__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'type'
// Member 'color'
// Member 'id'
// Member 'mission'
#include "rosidl_runtime_c/string.h"

// Struct defined in msg/Obj in the package obj_msg.
typedef struct obj_msg__msg__Obj
{
  rosidl_runtime_c__String type;
  rosidl_runtime_c__String color;
  rosidl_runtime_c__String id;
  rosidl_runtime_c__String mission;
} obj_msg__msg__Obj;

// Struct for a sequence of obj_msg__msg__Obj.
typedef struct obj_msg__msg__Obj__Sequence
{
  obj_msg__msg__Obj * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} obj_msg__msg__Obj__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // OBJ_MSG__MSG__DETAIL__OBJ__STRUCT_H_
