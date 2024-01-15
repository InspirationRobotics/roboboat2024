// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from obj_msg:msg/MapInfo.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__MAP_INFO__STRUCT_H_
#define OBJ_MSG__MSG__DETAIL__MAP_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/MapInfo in the package obj_msg.
typedef struct obj_msg__msg__MapInfo
{
  double origin_lat;
  double origin_lon;
  double hdg;
  double density;
  int64_t w;
  int64_t h;
} obj_msg__msg__MapInfo;

// Struct for a sequence of obj_msg__msg__MapInfo.
typedef struct obj_msg__msg__MapInfo__Sequence
{
  obj_msg__msg__MapInfo * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} obj_msg__msg__MapInfo__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // OBJ_MSG__MSG__DETAIL__MAP_INFO__STRUCT_H_
