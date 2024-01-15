// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from obj_msg:msg/MapInfo.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__MAP_INFO__STRUCT_HPP_
#define OBJ_MSG__MSG__DETAIL__MAP_INFO__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__obj_msg__msg__MapInfo __attribute__((deprecated))
#else
# define DEPRECATED__obj_msg__msg__MapInfo __declspec(deprecated)
#endif

namespace obj_msg
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MapInfo_
{
  using Type = MapInfo_<ContainerAllocator>;

  explicit MapInfo_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->origin_lat = 0.0;
      this->origin_lon = 0.0;
      this->hdg = 0.0;
      this->density = 0.0;
      this->w = 0ll;
      this->h = 0ll;
    }
  }

  explicit MapInfo_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->origin_lat = 0.0;
      this->origin_lon = 0.0;
      this->hdg = 0.0;
      this->density = 0.0;
      this->w = 0ll;
      this->h = 0ll;
    }
  }

  // field types and members
  using _origin_lat_type =
    double;
  _origin_lat_type origin_lat;
  using _origin_lon_type =
    double;
  _origin_lon_type origin_lon;
  using _hdg_type =
    double;
  _hdg_type hdg;
  using _density_type =
    double;
  _density_type density;
  using _w_type =
    int64_t;
  _w_type w;
  using _h_type =
    int64_t;
  _h_type h;

  // setters for named parameter idiom
  Type & set__origin_lat(
    const double & _arg)
  {
    this->origin_lat = _arg;
    return *this;
  }
  Type & set__origin_lon(
    const double & _arg)
  {
    this->origin_lon = _arg;
    return *this;
  }
  Type & set__hdg(
    const double & _arg)
  {
    this->hdg = _arg;
    return *this;
  }
  Type & set__density(
    const double & _arg)
  {
    this->density = _arg;
    return *this;
  }
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

  // constant declarations

  // pointer types
  using RawPtr =
    obj_msg::msg::MapInfo_<ContainerAllocator> *;
  using ConstRawPtr =
    const obj_msg::msg::MapInfo_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<obj_msg::msg::MapInfo_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<obj_msg::msg::MapInfo_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      obj_msg::msg::MapInfo_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<obj_msg::msg::MapInfo_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      obj_msg::msg::MapInfo_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<obj_msg::msg::MapInfo_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<obj_msg::msg::MapInfo_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<obj_msg::msg::MapInfo_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__obj_msg__msg__MapInfo
    std::shared_ptr<obj_msg::msg::MapInfo_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__obj_msg__msg__MapInfo
    std::shared_ptr<obj_msg::msg::MapInfo_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MapInfo_ & other) const
  {
    if (this->origin_lat != other.origin_lat) {
      return false;
    }
    if (this->origin_lon != other.origin_lon) {
      return false;
    }
    if (this->hdg != other.hdg) {
      return false;
    }
    if (this->density != other.density) {
      return false;
    }
    if (this->w != other.w) {
      return false;
    }
    if (this->h != other.h) {
      return false;
    }
    return true;
  }
  bool operator!=(const MapInfo_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MapInfo_

// alias to use template instance with default allocator
using MapInfo =
  obj_msg::msg::MapInfo_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace obj_msg

#endif  // OBJ_MSG__MSG__DETAIL__MAP_INFO__STRUCT_HPP_
