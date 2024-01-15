// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from obj_msg:msg/Obj.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "obj_msg/msg/detail/obj__rosidl_typesupport_introspection_c.h"
#include "obj_msg/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "obj_msg/msg/detail/obj__functions.h"
#include "obj_msg/msg/detail/obj__struct.h"


// Include directives for member types
// Member `type`
// Member `color`
// Member `id`
// Member `mission`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void Obj__rosidl_typesupport_introspection_c__Obj_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  obj_msg__msg__Obj__init(message_memory);
}

void Obj__rosidl_typesupport_introspection_c__Obj_fini_function(void * message_memory)
{
  obj_msg__msg__Obj__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember Obj__rosidl_typesupport_introspection_c__Obj_message_member_array[4] = {
  {
    "type",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg__msg__Obj, type),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "color",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg__msg__Obj, color),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg__msg__Obj, id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "mission",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg__msg__Obj, mission),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers Obj__rosidl_typesupport_introspection_c__Obj_message_members = {
  "obj_msg__msg",  // message namespace
  "Obj",  // message name
  4,  // number of fields
  sizeof(obj_msg__msg__Obj),
  Obj__rosidl_typesupport_introspection_c__Obj_message_member_array,  // message members
  Obj__rosidl_typesupport_introspection_c__Obj_init_function,  // function to initialize message memory (memory has to be allocated)
  Obj__rosidl_typesupport_introspection_c__Obj_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t Obj__rosidl_typesupport_introspection_c__Obj_message_type_support_handle = {
  0,
  &Obj__rosidl_typesupport_introspection_c__Obj_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_obj_msg
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, obj_msg, msg, Obj)() {
  if (!Obj__rosidl_typesupport_introspection_c__Obj_message_type_support_handle.typesupport_identifier) {
    Obj__rosidl_typesupport_introspection_c__Obj_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &Obj__rosidl_typesupport_introspection_c__Obj_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
