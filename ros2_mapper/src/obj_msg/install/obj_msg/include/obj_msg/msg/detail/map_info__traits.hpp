// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from obj_msg:msg/MapInfo.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__MAP_INFO__TRAITS_HPP_
#define OBJ_MSG__MSG__DETAIL__MAP_INFO__TRAITS_HPP_

#include "obj_msg/msg/detail/map_info__struct.hpp"
#include <stdint.h>
#include <rosidl_runtime_cpp/traits.hpp>
#include <sstream>
#include <string>
#include <type_traits>

namespace rosidl_generator_traits
{

inline void to_yaml(
  const obj_msg::msg::MapInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: origin_lat
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "origin_lat: ";
    value_to_yaml(msg.origin_lat, out);
    out << "\n";
  }

  // member: origin_lon
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "origin_lon: ";
    value_to_yaml(msg.origin_lon, out);
    out << "\n";
  }

  // member: hdg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "hdg: ";
    value_to_yaml(msg.hdg, out);
    out << "\n";
  }

  // member: density
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "density: ";
    value_to_yaml(msg.density, out);
    out << "\n";
  }

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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const obj_msg::msg::MapInfo & msg)
{
  std::ostringstream out;
  to_yaml(msg, out);
  return out.str();
}

template<>
inline const char * data_type<obj_msg::msg::MapInfo>()
{
  return "obj_msg::msg::MapInfo";
}

template<>
inline const char * name<obj_msg::msg::MapInfo>()
{
  return "obj_msg/msg/MapInfo";
}

template<>
struct has_fixed_size<obj_msg::msg::MapInfo>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<obj_msg::msg::MapInfo>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<obj_msg::msg::MapInfo>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // OBJ_MSG__MSG__DETAIL__MAP_INFO__TRAITS_HPP_
