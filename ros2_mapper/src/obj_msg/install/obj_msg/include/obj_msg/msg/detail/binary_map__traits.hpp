// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from obj_msg:msg/BinaryMap.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__BINARY_MAP__TRAITS_HPP_
#define OBJ_MSG__MSG__DETAIL__BINARY_MAP__TRAITS_HPP_

#include "obj_msg/msg/detail/binary_map__struct.hpp"
#include <stdint.h>
#include <rosidl_runtime_cpp/traits.hpp>
#include <sstream>
#include <string>
#include <type_traits>

// Include directives for member types
// Member 'm'
#include "obj_msg/msg/detail/map_info__traits.hpp"

namespace rosidl_generator_traits
{

inline void to_yaml(
  const obj_msg::msg::BinaryMap & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: m
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "m:\n";
    to_yaml(msg.m, out, indentation + 2);
  }

  // member: objects
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.objects.size() == 0) {
      out << "objects: []\n";
    } else {
      out << "objects:\n";
      for (auto item : msg.objects) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const obj_msg::msg::BinaryMap & msg)
{
  std::ostringstream out;
  to_yaml(msg, out);
  return out.str();
}

template<>
inline const char * data_type<obj_msg::msg::BinaryMap>()
{
  return "obj_msg::msg::BinaryMap";
}

template<>
inline const char * name<obj_msg::msg::BinaryMap>()
{
  return "obj_msg/msg/BinaryMap";
}

template<>
struct has_fixed_size<obj_msg::msg::BinaryMap>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<obj_msg::msg::BinaryMap>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<obj_msg::msg::BinaryMap>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // OBJ_MSG__MSG__DETAIL__BINARY_MAP__TRAITS_HPP_
