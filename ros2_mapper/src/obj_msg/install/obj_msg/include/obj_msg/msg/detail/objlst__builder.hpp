// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from obj_msg:msg/Objlst.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__OBJLST__BUILDER_HPP_
#define OBJ_MSG__MSG__DETAIL__OBJLST__BUILDER_HPP_

#include "obj_msg/msg/detail/objlst__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace obj_msg
{

namespace msg
{

namespace builder
{

class Init_Objlst_objects
{
public:
  explicit Init_Objlst_objects(::obj_msg::msg::Objlst & msg)
  : msg_(msg)
  {}
  ::obj_msg::msg::Objlst objects(::obj_msg::msg::Objlst::_objects_type arg)
  {
    msg_.objects = std::move(arg);
    return std::move(msg_);
  }

private:
  ::obj_msg::msg::Objlst msg_;
};

class Init_Objlst_h
{
public:
  explicit Init_Objlst_h(::obj_msg::msg::Objlst & msg)
  : msg_(msg)
  {}
  Init_Objlst_objects h(::obj_msg::msg::Objlst::_h_type arg)
  {
    msg_.h = std::move(arg);
    return Init_Objlst_objects(msg_);
  }

private:
  ::obj_msg::msg::Objlst msg_;
};

class Init_Objlst_w
{
public:
  Init_Objlst_w()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Objlst_h w(::obj_msg::msg::Objlst::_w_type arg)
  {
    msg_.w = std::move(arg);
    return Init_Objlst_h(msg_);
  }

private:
  ::obj_msg::msg::Objlst msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::obj_msg::msg::Objlst>()
{
  return obj_msg::msg::builder::Init_Objlst_w();
}

}  // namespace obj_msg

#endif  // OBJ_MSG__MSG__DETAIL__OBJLST__BUILDER_HPP_
