// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from obj_msg:msg/BinaryMap.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "obj_msg/msg/detail/binary_map__rosidl_typesupport_introspection_c.h"
#include "obj_msg/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "obj_msg/msg/detail/binary_map__functions.h"
#include "obj_msg/msg/detail/binary_map__struct.h"


// Include directives for member types
// Member `m`
#include "obj_msg/msg/map_info.h"
// Member `m`
#include "obj_msg/msg/detail/map_info__rosidl_typesupport_introspection_c.h"
// Member `objects`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void BinaryMap__rosidl_typesupport_introspection_c__BinaryMap_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  obj_msg__msg__BinaryMap__init(message_memory);
}

void BinaryMap__rosidl_typesupport_introspection_c__BinaryMap_fini_function(void * message_memory)
{
  obj_msg__msg__BinaryMap__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember BinaryMap__rosidl_typesupport_introspection_c__BinaryMap_message_member_array[2] = {
  {
    "m",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg__msg__BinaryMap, m),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "objects",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg__msg__BinaryMap, objects),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers BinaryMap__rosidl_typesupport_introspection_c__BinaryMap_message_members = {
  "obj_msg__msg",  // message namespace
  "BinaryMap",  // message name
  2,  // number of fields
  sizeof(obj_msg__msg__BinaryMap),
  BinaryMap__rosidl_typesupport_introspection_c__BinaryMap_message_member_array,  // message members
  BinaryMap__rosidl_typesupport_introspection_c__BinaryMap_init_function,  // function to initialize message memory (memory has to be allocated)
  BinaryMap__rosidl_typesupport_introspection_c__BinaryMap_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t BinaryMap__rosidl_typesupport_introspection_c__BinaryMap_message_type_support_handle = {
  0,
  &BinaryMap__rosidl_typesupport_introspection_c__BinaryMap_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_obj_msg
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, obj_msg, msg, BinaryMap)() {
  BinaryMap__rosidl_typesupport_introspection_c__BinaryMap_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, obj_msg, msg, MapInfo)();
  if (!BinaryMap__rosidl_typesupport_introspection_c__BinaryMap_message_type_support_handle.typesupport_identifier) {
    BinaryMap__rosidl_typesupport_introspection_c__BinaryMap_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &BinaryMap__rosidl_typesupport_introspection_c__BinaryMap_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
