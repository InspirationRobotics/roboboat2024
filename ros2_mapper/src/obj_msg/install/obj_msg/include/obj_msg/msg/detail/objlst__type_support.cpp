// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from obj_msg:msg/Objlst.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "obj_msg/msg/detail/objlst__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace obj_msg
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void Objlst_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) obj_msg::msg::Objlst(_init);
}

void Objlst_fini_function(void * message_memory)
{
  auto typed_message = static_cast<obj_msg::msg::Objlst *>(message_memory);
  typed_message->~Objlst();
}

size_t size_function__Objlst__objects(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<obj_msg::msg::Obj> *>(untyped_member);
  return member->size();
}

const void * get_const_function__Objlst__objects(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<obj_msg::msg::Obj> *>(untyped_member);
  return &member[index];
}

void * get_function__Objlst__objects(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<obj_msg::msg::Obj> *>(untyped_member);
  return &member[index];
}

void resize_function__Objlst__objects(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<obj_msg::msg::Obj> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember Objlst_message_member_array[3] = {
  {
    "w",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg::msg::Objlst, w),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "h",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg::msg::Objlst, h),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "objects",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<obj_msg::msg::Obj>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(obj_msg::msg::Objlst, objects),  // bytes offset in struct
    nullptr,  // default value
    size_function__Objlst__objects,  // size() function pointer
    get_const_function__Objlst__objects,  // get_const(index) function pointer
    get_function__Objlst__objects,  // get(index) function pointer
    resize_function__Objlst__objects  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers Objlst_message_members = {
  "obj_msg::msg",  // message namespace
  "Objlst",  // message name
  3,  // number of fields
  sizeof(obj_msg::msg::Objlst),
  Objlst_message_member_array,  // message members
  Objlst_init_function,  // function to initialize message memory (memory has to be allocated)
  Objlst_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t Objlst_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &Objlst_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace obj_msg


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<obj_msg::msg::Objlst>()
{
  return &::obj_msg::msg::rosidl_typesupport_introspection_cpp::Objlst_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, obj_msg, msg, Objlst)() {
  return &::obj_msg::msg::rosidl_typesupport_introspection_cpp::Objlst_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
