// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from obj_msg:msg/Map.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "obj_msg/msg/detail/map__rosidl_typesupport_introspection_c.h"
#include "obj_msg/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "obj_msg/msg/detail/map__functions.h"
#include "obj_msg/msg/detail/map__struct.h"


// Include directives for member types
// Member `origin`
#include "rosidl_runtime_c/primitives_sequence_functions.h"
// Member `objects`
#include "obj_msg/msg/obj.h"
// Member `objects`
#include "obj_msg/msg/detail/obj__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void Map__rosidl_typesupport_introspection_c__Map_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  obj_msg__msg__Map__init(message_memory);
}

void Map__rosidl_typesupport_introspection_c__Map_fini_function(void * message_memory)
{
  obj_msg__msg__Map__fini(message_memory);
}

size_t Map__rosidl_typesupport_introspection_c__size_function__Obj__objects(
  const void * untyped_member)
{
  const obj_msg__msg__Obj__Sequence * member =
    (const obj_msg__msg__Obj__Sequence *)(untyped_member);
  return member->size;
}

const void * Map__rosidl_typesupport_introspection_c__get_const_function__Obj__objects(
  const void * untyped_member, size_t index)
{
  const obj_msg__msg__Obj__Sequence * member =
    (const obj_msg__msg__Obj__Sequence *)(untyped_member);
  return &member->data[index];
}

void * Map__rosidl_typesupport_introspection_c__get_function__Obj__objects(
  void * untyped_member, size_t index)
{
  obj_msg__msg__Obj__Sequence * member =
    (obj_msg__msg__Obj__Sequence *)(untyped_member);
  return &member->data[index];
}

bool Map__rosidl_typesupport_introspection_c__resize_function__Obj__objects(
  void * untyped_member, size_t size)
{
  obj_msg__msg__Obj__Sequence * member =
    (obj_msg__msg__Obj__Sequence *)(untyped_member);
  obj_msg__msg__Obj__Sequence__fini(member);
  return obj_msg__msg__Obj__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember Map__rosidl_typesupport_introspection_c__Map_message_member_array[6] = {
  {
    "w",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg__msg__Map, w),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "h",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg__msg__Map, h),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "origin",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg__msg__Map, origin),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "heading",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg__msg__Map, heading),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "density",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg__msg__Map, density),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "objects",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg__msg__Map, objects),  // bytes offset in struct
    NULL,  // default value
    Map__rosidl_typesupport_introspection_c__size_function__Obj__objects,  // size() function pointer
    Map__rosidl_typesupport_introspection_c__get_const_function__Obj__objects,  // get_const(index) function pointer
    Map__rosidl_typesupport_introspection_c__get_function__Obj__objects,  // get(index) function pointer
    Map__rosidl_typesupport_introspection_c__resize_function__Obj__objects  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers Map__rosidl_typesupport_introspection_c__Map_message_members = {
  "obj_msg__msg",  // message namespace
  "Map",  // message name
  6,  // number of fields
  sizeof(obj_msg__msg__Map),
  Map__rosidl_typesupport_introspection_c__Map_message_member_array,  // message members
  Map__rosidl_typesupport_introspection_c__Map_init_function,  // function to initialize message memory (memory has to be allocated)
  Map__rosidl_typesupport_introspection_c__Map_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t Map__rosidl_typesupport_introspection_c__Map_message_type_support_handle = {
  0,
  &Map__rosidl_typesupport_introspection_c__Map_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_obj_msg
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, obj_msg, msg, Map)() {
  Map__rosidl_typesupport_introspection_c__Map_message_member_array[5].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, obj_msg, msg, Obj)();
  if (!Map__rosidl_typesupport_introspection_c__Map_message_type_support_handle.typesupport_identifier) {
    Map__rosidl_typesupport_introspection_c__Map_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &Map__rosidl_typesupport_introspection_c__Map_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
