// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from obj_msg:msg/BinaryMap.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__BINARY_MAP__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define OBJ_MSG__MSG__DETAIL__BINARY_MAP__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "obj_msg/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "obj_msg/msg/detail/binary_map__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace obj_msg
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_obj_msg
cdr_serialize(
  const obj_msg::msg::BinaryMap & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_obj_msg
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  obj_msg::msg::BinaryMap & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_obj_msg
get_serialized_size(
  const obj_msg::msg::BinaryMap & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_obj_msg
max_serialized_size_BinaryMap(
  bool & full_bounded,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace obj_msg

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_obj_msg
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, obj_msg, msg, BinaryMap)();

#ifdef __cplusplus
}
#endif

#endif  // OBJ_MSG__MSG__DETAIL__BINARY_MAP__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
