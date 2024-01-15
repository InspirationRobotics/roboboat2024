// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from obj_msg:msg/Objlst.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__OBJLST__STRUCT_H_
#define OBJ_MSG__MSG__DETAIL__OBJLST__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'objects'
#include "obj_msg/msg/detail/obj__struct.h"

// Struct defined in msg/Objlst in the package obj_msg.
typedef struct obj_msg__msg__Objlst
{
  int64_t w;
  int64_t h;
  obj_msg__msg__Obj__Sequence objects;
} obj_msg__msg__Objlst;

// Struct for a sequence of obj_msg__msg__Objlst.
typedef struct obj_msg__msg__Objlst__Sequence
{
  obj_msg__msg__Objlst * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} obj_msg__msg__Objlst__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // OBJ_MSG__MSG__DETAIL__OBJLST__STRUCT_H_
