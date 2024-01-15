// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from obj_msg:msg/Obj.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__OBJ__TRAITS_HPP_
#define OBJ_MSG__MSG__DETAIL__OBJ__TRAITS_HPP_

#include "obj_msg/msg/detail/obj__struct.hpp"
#include <stdint.h>
#include <rosidl_runtime_cpp/traits.hpp>
#include <sstream>
#include <string>
#include <type_traits>

namespace rosidl_generator_traits
{

inline void to_yaml(
  const obj_msg::msg::Obj & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "type: ";
    value_to_yaml(msg.type, out);
    out << "\n";
  }

  // member: color
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "color: ";
    value_to_yaml(msg.color, out);
    out << "\n";
  }

  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    value_to_yaml(msg.id, out);
    out << "\n";
  }

  // member: mission
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mission: ";
    value_to_yaml(msg.mission, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const obj_msg::msg::Obj & msg)
{
  std::ostringstream out;
  to_yaml(msg, out);
  return out.str();
}

template<>
inline const char * data_type<obj_msg::msg::Obj>()
{
  return "obj_msg::msg::Obj";
}

template<>
inline const char * name<obj_msg::msg::Obj>()
{
  return "obj_msg/msg/Obj";
}

template<>
struct has_fixed_size<obj_msg::msg::Obj>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<obj_msg::msg::Obj>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<obj_msg::msg::Obj>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // OBJ_MSG__MSG__DETAIL__OBJ__TRAITS_HPP_
