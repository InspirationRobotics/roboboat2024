// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from obj_msg:msg/Map.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__MAP__STRUCT_HPP_
#define OBJ_MSG__MSG__DETAIL__MAP__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


// Include directives for member types
// Member 'm'
#include "obj_msg/msg/detail/map_info__struct.hpp"
// Member 'objects'
#include "obj_msg/msg/detail/obj__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__obj_msg__msg__Map __attribute__((deprecated))
#else
# define DEPRECATED__obj_msg__msg__Map __declspec(deprecated)
#endif

namespace obj_msg
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Map_
{
  using Type = Map_<ContainerAllocator>;

  explicit Map_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : m(_init)
  {
    (void)_init;
  }

  explicit Map_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : m(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _m_type =
    obj_msg::msg::MapInfo_<ContainerAllocator>;
  _m_type m;
  using _objects_type =
    std::vector<obj_msg::msg::Obj_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<obj_msg::msg::Obj_<ContainerAllocator>>>;
  _objects_type objects;

  // setters for named parameter idiom
  Type & set__m(
    const obj_msg::msg::MapInfo_<ContainerAllocator> & _arg)
  {
    this->m = _arg;
    return *this;
  }
  Type & set__objects(
    const std::vector<obj_msg::msg::Obj_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<obj_msg::msg::Obj_<ContainerAllocator>>> & _arg)
  {
    this->objects = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    obj_msg::msg::Map_<ContainerAllocator> *;
  using ConstRawPtr =
    const obj_msg::msg::Map_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<obj_msg::msg::Map_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<obj_msg::msg::Map_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      obj_msg::msg::Map_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<obj_msg::msg::Map_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      obj_msg::msg::Map_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<obj_msg::msg::Map_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<obj_msg::msg::Map_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<obj_msg::msg::Map_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__obj_msg__msg__Map
    std::shared_ptr<obj_msg::msg::Map_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__obj_msg__msg__Map
    std::shared_ptr<obj_msg::msg::Map_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Map_ & other) const
  {
    if (this->m != other.m) {
      return false;
    }
    if (this->objects != other.objects) {
      return false;
    }
    return true;
  }
  bool operator!=(const Map_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Map_

// alias to use template instance with default allocator
using Map =
  obj_msg::msg::Map_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace obj_msg

#endif  // OBJ_MSG__MSG__DETAIL__MAP__STRUCT_HPP_
