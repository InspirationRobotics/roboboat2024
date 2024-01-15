// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from obj_msg:msg/Objlst.idl
// generated code does not contain a copyright notice

#ifndef OBJ_MSG__MSG__DETAIL__OBJLST__FUNCTIONS_H_
#define OBJ_MSG__MSG__DETAIL__OBJLST__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "obj_msg/msg/rosidl_generator_c__visibility_control.h"

#include "obj_msg/msg/detail/objlst__struct.h"

/// Initialize msg/Objlst message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * obj_msg__msg__Objlst
 * )) before or use
 * obj_msg__msg__Objlst__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_obj_msg
bool
obj_msg__msg__Objlst__init(obj_msg__msg__Objlst * msg);

/// Finalize msg/Objlst message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_obj_msg
void
obj_msg__msg__Objlst__fini(obj_msg__msg__Objlst * msg);

/// Create msg/Objlst message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * obj_msg__msg__Objlst__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_obj_msg
obj_msg__msg__Objlst *
obj_msg__msg__Objlst__create();

/// Destroy msg/Objlst message.
/**
 * It calls
 * obj_msg__msg__Objlst__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_obj_msg
void
obj_msg__msg__Objlst__destroy(obj_msg__msg__Objlst * msg);

/// Check for msg/Objlst message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_obj_msg
bool
obj_msg__msg__Objlst__are_equal(const obj_msg__msg__Objlst * lhs, const obj_msg__msg__Objlst * rhs);

/// Copy a msg/Objlst message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_obj_msg
bool
obj_msg__msg__Objlst__copy(
  const obj_msg__msg__Objlst * input,
  obj_msg__msg__Objlst * output);

/// Initialize array of msg/Objlst messages.
/**
 * It allocates the memory for the number of elements and calls
 * obj_msg__msg__Objlst__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_obj_msg
bool
obj_msg__msg__Objlst__Sequence__init(obj_msg__msg__Objlst__Sequence * array, size_t size);

/// Finalize array of msg/Objlst messages.
/**
 * It calls
 * obj_msg__msg__Objlst__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_obj_msg
void
obj_msg__msg__Objlst__Sequence__fini(obj_msg__msg__Objlst__Sequence * array);

/// Create array of msg/Objlst messages.
/**
 * It allocates the memory for the array and calls
 * obj_msg__msg__Objlst__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_obj_msg
obj_msg__msg__Objlst__Sequence *
obj_msg__msg__Objlst__Sequence__create(size_t size);

/// Destroy array of msg/Objlst messages.
/**
 * It calls
 * obj_msg__msg__Objlst__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_obj_msg
void
obj_msg__msg__Objlst__Sequence__destroy(obj_msg__msg__Objlst__Sequence * array);

/// Check for msg/Objlst message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_obj_msg
bool
obj_msg__msg__Objlst__Sequence__are_equal(const obj_msg__msg__Objlst__Sequence * lhs, const obj_msg__msg__Objlst__Sequence * rhs);

/// Copy an array of msg/Objlst messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_obj_msg
bool
obj_msg__msg__Objlst__Sequence__copy(
  const obj_msg__msg__Objlst__Sequence * input,
  obj_msg__msg__Objlst__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // OBJ_MSG__MSG__DETAIL__OBJLST__FUNCTIONS_H_
