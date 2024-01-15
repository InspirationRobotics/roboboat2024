// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from obj_msg:msg/Obj.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__OBJ__BUILDER_HPP_
#define OBJ_MSG__MSG__DETAIL__OBJ__BUILDER_HPP_

#include "obj_msg/msg/detail/obj__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace obj_msg
{

namespace msg
{

namespace builder
{

class Init_Obj_mission
{
public:
  explicit Init_Obj_mission(::obj_msg::msg::Obj & msg)
  : msg_(msg)
  {}
  ::obj_msg::msg::Obj mission(::obj_msg::msg::Obj::_mission_type arg)
  {
    msg_.mission = std::move(arg);
    return std::move(msg_);
  }

private:
  ::obj_msg::msg::Obj msg_;
};

class Init_Obj_id
{
public:
  explicit Init_Obj_id(::obj_msg::msg::Obj & msg)
  : msg_(msg)
  {}
  Init_Obj_mission id(::obj_msg::msg::Obj::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_Obj_mission(msg_);
  }

private:
  ::obj_msg::msg::Obj msg_;
};

class Init_Obj_color
{
public:
  explicit Init_Obj_color(::obj_msg::msg::Obj & msg)
  : msg_(msg)
  {}
  Init_Obj_id color(::obj_msg::msg::Obj::_color_type arg)
  {
    msg_.color = std::move(arg);
    return Init_Obj_id(msg_);
  }

private:
  ::obj_msg::msg::Obj msg_;
};

class Init_Obj_type
{
public:
  Init_Obj_type()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Obj_color type(::obj_msg::msg::Obj::_type_type arg)
  {
    msg_.type = std::move(arg);
    return Init_Obj_color(msg_);
  }

private:
  ::obj_msg::msg::Obj msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::obj_msg::msg::Obj>()
{
  return obj_msg::msg::builder::Init_Obj_type();
}

}  // namespace obj_msg

#endif  // OBJ_MSG__MSG__DETAIL__OBJ__BUILDER_HPP_
