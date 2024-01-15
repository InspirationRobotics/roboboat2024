// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from obj_msg:msg/Objlst.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "obj_msg/msg/detail/objlst__rosidl_typesupport_introspection_c.h"
#include "obj_msg/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "obj_msg/msg/detail/objlst__functions.h"
#include "obj_msg/msg/detail/objlst__struct.h"


// Include directives for member types
// Member `objects`
#include "obj_msg/msg/obj.h"
// Member `objects`
#include "obj_msg/msg/detail/obj__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void Objlst__rosidl_typesupport_introspection_c__Objlst_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  obj_msg__msg__Objlst__init(message_memory);
}

void Objlst__rosidl_typesupport_introspection_c__Objlst_fini_function(void * message_memory)
{
  obj_msg__msg__Objlst__fini(message_memory);
}

size_t Objlst__rosidl_typesupport_introspection_c__size_function__Obj__objects(
  const void * untyped_member)
{
  const obj_msg__msg__Obj__Sequence * member =
    (const obj_msg__msg__Obj__Sequence *)(untyped_member);
  return member->size;
}

const void * Objlst__rosidl_typesupport_introspection_c__get_const_function__Obj__objects(
  const void * untyped_member, size_t index)
{
  const obj_msg__msg__Obj__Sequence * member =
    (const obj_msg__msg__Obj__Sequence *)(untyped_member);
  return &member->data[index];
}

void * Objlst__rosidl_typesupport_introspection_c__get_function__Obj__objects(
  void * untyped_member, size_t index)
{
  obj_msg__msg__Obj__Sequence * member =
    (obj_msg__msg__Obj__Sequence *)(untyped_member);
  return &member->data[index];
}

bool Objlst__rosidl_typesupport_introspection_c__resize_function__Obj__objects(
  void * untyped_member, size_t size)
{
  obj_msg__msg__Obj__Sequence * member =
    (obj_msg__msg__Obj__Sequence *)(untyped_member);
  obj_msg__msg__Obj__Sequence__fini(member);
  return obj_msg__msg__Obj__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember Objlst__rosidl_typesupport_introspection_c__Objlst_message_member_array[3] = {
  {
    "w",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg__msg__Objlst, w),  // bytes offset in struct
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
    offsetof(obj_msg__msg__Objlst, h),  // bytes offset in struct
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
    offsetof(obj_msg__msg__Objlst, objects),  // bytes offset in struct
    NULL,  // default value
    Objlst__rosidl_typesupport_introspection_c__size_function__Obj__objects,  // size() function pointer
    Objlst__rosidl_typesupport_introspection_c__get_const_function__Obj__objects,  // get_const(index) function pointer
    Objlst__rosidl_typesupport_introspection_c__get_function__Obj__objects,  // get(index) function pointer
    Objlst__rosidl_typesupport_introspection_c__resize_function__Obj__objects  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers Objlst__rosidl_typesupport_introspection_c__Objlst_message_members = {
  "obj_msg__msg",  // message namespace
  "Objlst",  // message name
  3,  // number of fields
  sizeof(obj_msg__msg__Objlst),
  Objlst__rosidl_typesupport_introspection_c__Objlst_message_member_array,  // message members
  Objlst__rosidl_typesupport_introspection_c__Objlst_init_function,  // function to initialize message memory (memory has to be allocated)
  Objlst__rosidl_typesupport_introspection_c__Objlst_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t Objlst__rosidl_typesupport_introspection_c__Objlst_message_type_support_handle = {
  0,
  &Objlst__rosidl_typesupport_introspection_c__Objlst_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_obj_msg
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, obj_msg, msg, Objlst)() {
  Objlst__rosidl_typesupport_introspection_c__Objlst_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, obj_msg, msg, Obj)();
  if (!Objlst__rosidl_typesupport_introspection_c__Objlst_message_type_support_handle.typesupport_identifier) {
    Objlst__rosidl_typesupport_introspection_c__Objlst_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &Objlst__rosidl_typesupport_introspection_c__Objlst_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
