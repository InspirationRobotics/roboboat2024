// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from obj_msg:msg/Objlst.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__OBJLST__TRAITS_HPP_
#define OBJ_MSG__MSG__DETAIL__OBJLST__TRAITS_HPP_

#include "obj_msg/msg/detail/objlst__struct.hpp"
#include <stdint.h>
#include <rosidl_runtime_cpp/traits.hpp>
#include <sstream>
#include <string>
#include <type_traits>

// Include directives for member types
// Member 'objects'
#include "obj_msg/msg/detail/obj__traits.hpp"

namespace rosidl_generator_traits
{

inline void to_yaml(
  const obj_msg::msg::Objlst & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: w
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "w: ";
    value_to_yaml(msg.w, out);
    out << "\n";
  }

  // member: h
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "h: ";
    value_to_yaml(msg.h, out);
    out << "\n";
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
        out << "-\n";
        to_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const obj_msg::msg::Objlst & msg)
{
  std::ostringstream out;
  to_yaml(msg, out);
  return out.str();
}

template<>
inline const char * data_type<obj_msg::msg::Objlst>()
{
  return "obj_msg::msg::Objlst";
}

template<>
inline const char * name<obj_msg::msg::Objlst>()
{
  return "obj_msg/msg/Objlst";
}

template<>
struct has_fixed_size<obj_msg::msg::Objlst>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<obj_msg::msg::Objlst>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<obj_msg::msg::Objlst>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // OBJ_MSG__MSG__DETAIL__OBJLST__TRAITS_HPP_
