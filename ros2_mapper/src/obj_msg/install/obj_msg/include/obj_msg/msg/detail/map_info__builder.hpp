// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from obj_msg:msg/MapInfo.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__MAP_INFO__BUILDER_HPP_
#define OBJ_MSG__MSG__DETAIL__MAP_INFO__BUILDER_HPP_

#include "obj_msg/msg/detail/map_info__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace obj_msg
{

namespace msg
{

namespace builder
{

class Init_MapInfo_h
{
public:
  explicit Init_MapInfo_h(::obj_msg::msg::MapInfo & msg)
  : msg_(msg)
  {}
  ::obj_msg::msg::MapInfo h(::obj_msg::msg::MapInfo::_h_type arg)
  {
    msg_.h = std::move(arg);
    return std::move(msg_);
  }

private:
  ::obj_msg::msg::MapInfo msg_;
};

class Init_MapInfo_w
{
public:
  explicit Init_MapInfo_w(::obj_msg::msg::MapInfo & msg)
  : msg_(msg)
  {}
  Init_MapInfo_h w(::obj_msg::msg::MapInfo::_w_type arg)
  {
    msg_.w = std::move(arg);
    return Init_MapInfo_h(msg_);
  }

private:
  ::obj_msg::msg::MapInfo msg_;
};

class Init_MapInfo_density
{
public:
  explicit Init_MapInfo_density(::obj_msg::msg::MapInfo & msg)
  : msg_(msg)
  {}
  Init_MapInfo_w density(::obj_msg::msg::MapInfo::_density_type arg)
  {
    msg_.density = std::move(arg);
    return Init_MapInfo_w(msg_);
  }

private:
  ::obj_msg::msg::MapInfo msg_;
};

class Init_MapInfo_hdg
{
public:
  explicit Init_MapInfo_hdg(::obj_msg::msg::MapInfo & msg)
  : msg_(msg)
  {}
  Init_MapInfo_density hdg(::obj_msg::msg::MapInfo::_hdg_type arg)
  {
    msg_.hdg = std::move(arg);
    return Init_MapInfo_density(msg_);
  }

private:
  ::obj_msg::msg::MapInfo msg_;
};

class Init_MapInfo_origin_lon
{
public:
  explicit Init_MapInfo_origin_lon(::obj_msg::msg::MapInfo & msg)
  : msg_(msg)
  {}
  Init_MapInfo_hdg origin_lon(::obj_msg::msg::MapInfo::_origin_lon_type arg)
  {
    msg_.origin_lon = std::move(arg);
    return Init_MapInfo_hdg(msg_);
  }

private:
  ::obj_msg::msg::MapInfo msg_;
};

class Init_MapInfo_origin_lat
{
public:
  Init_MapInfo_origin_lat()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MapInfo_origin_lon origin_lat(::obj_msg::msg::MapInfo::_origin_lat_type arg)
  {
    msg_.origin_lat = std::move(arg);
    return Init_MapInfo_origin_lon(msg_);
  }

private:
  ::obj_msg::msg::MapInfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::obj_msg::msg::MapInfo>()
{
  return obj_msg::msg::builder::Init_MapInfo_origin_lat();
}

}  // namespace obj_msg

#endif  // OBJ_MSG__MSG__DETAIL__MAP_INFO__BUILDER_HPP_
