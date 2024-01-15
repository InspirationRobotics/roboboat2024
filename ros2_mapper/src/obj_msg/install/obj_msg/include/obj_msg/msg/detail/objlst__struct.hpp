// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from obj_msg:msg/Objlst.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__OBJLST__STRUCT_HPP_
#define OBJ_MSG__MSG__DETAIL__OBJLST__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


// Include directives for member types
// Member 'objects'
#include "obj_msg/msg/detail/obj__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__obj_msg__msg__Objlst __attribute__((deprecated))
#else
# define DEPRECATED__obj_msg__msg__Objlst __declspec(deprecated)
#endif

namespace obj_msg
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Objlst_
{
  using Type = Objlst_<ContainerAllocator>;

  explicit Objlst_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->w = 0ll;
      this->h = 0ll;
    }
  }

  explicit Objlst_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->w = 0ll;
      this->h = 0ll;
    }
  }

  // field types and members
  using _w_type =
    int64_t;
  _w_type w;
  using _h_type =
    int64_t;
  _h_type h;
  using _objects_type =
    std::vector<obj_msg::msg::Obj_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<obj_msg::msg::Obj_<ContainerAllocator>>>;
  _objects_type objects;

  // setters for named parameter idiom
  Type & set__w(
    const int64_t & _arg)
  {
    this->w = _arg;
    return *this;
  }
  Type & set__h(
    const int64_t & _arg)
  {
    this->h = _arg;
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
    obj_msg::msg::Objlst_<ContainerAllocator> *;
  using ConstRawPtr =
    const obj_msg::msg::Objlst_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<obj_msg::msg::Objlst_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<obj_msg::msg::Objlst_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      obj_msg::msg::Objlst_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<obj_msg::msg::Objlst_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      obj_msg::msg::Objlst_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<obj_msg::msg::Objlst_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<obj_msg::msg::Objlst_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<obj_msg::msg::Objlst_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__obj_msg__msg__Objlst
    std::shared_ptr<obj_msg::msg::Objlst_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__obj_msg__msg__Objlst
    std::shared_ptr<obj_msg::msg::Objlst_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Objlst_ & other) const
  {
    if (this->w != other.w) {
      return false;
    }
    if (this->h != other.h) {
      return false;
    }
    if (this->objects != other.objects) {
      return false;
    }
    return true;
  }
  bool operator!=(const Objlst_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Objlst_

// alias to use template instance with default allocator
using Objlst =
  obj_msg::msg::Objlst_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace obj_msg

#endif  // OBJ_MSG__MSG__DETAIL__OBJLST__STRUCT_HPP_
