// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from obj_msg:msg/BinaryMap.idl
// generated code does not contain a copyright notice
#include "obj_msg/msg/detail/binary_map__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


// Include directives for member types
// Member `m`
#include "obj_msg/msg/detail/map_info__functions.h"
// Member `objects`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
obj_msg__msg__BinaryMap__init(obj_msg__msg__BinaryMap * msg)
{
  if (!msg) {
    return false;
  }
  // m
  if (!obj_msg__msg__MapInfo__init(&msg->m)) {
    obj_msg__msg__BinaryMap__fini(msg);
    return false;
  }
  // objects
  if (!rosidl_runtime_c__int64__Sequence__init(&msg->objects, 0)) {
    obj_msg__msg__BinaryMap__fini(msg);
    return false;
  }
  return true;
}

void
obj_msg__msg__BinaryMap__fini(obj_msg__msg__BinaryMap * msg)
{
  if (!msg) {
    return;
  }
  // m
  obj_msg__msg__MapInfo__fini(&msg->m);
  // objects
  rosidl_runtime_c__int64__Sequence__fini(&msg->objects);
}

bool
obj_msg__msg__BinaryMap__are_equal(const obj_msg__msg__BinaryMap * lhs, const obj_msg__msg__BinaryMap * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // m
  if (!obj_msg__msg__MapInfo__are_equal(
      &(lhs->m), &(rhs->m)))
  {
    return false;
  }
  // objects
  if (!rosidl_runtime_c__int64__Sequence__are_equal(
      &(lhs->objects), &(rhs->objects)))
  {
    return false;
  }
  return true;
}

bool
obj_msg__msg__BinaryMap__copy(
  const obj_msg__msg__BinaryMap * input,
  obj_msg__msg__BinaryMap * output)
{
  if (!input || !output) {
    return false;
  }
  // m
  if (!obj_msg__msg__MapInfo__copy(
      &(input->m), &(output->m)))
  {
    return false;
  }
  // objects
  if (!rosidl_runtime_c__int64__Sequence__copy(
      &(input->objects), &(output->objects)))
  {
    return false;
  }
  return true;
}

obj_msg__msg__BinaryMap *
obj_msg__msg__BinaryMap__create()
{
  obj_msg__msg__BinaryMap * msg = (obj_msg__msg__BinaryMap *)malloc(sizeof(obj_msg__msg__BinaryMap));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(obj_msg__msg__BinaryMap));
  bool success = obj_msg__msg__BinaryMap__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
obj_msg__msg__BinaryMap__destroy(obj_msg__msg__BinaryMap * msg)
{
  if (msg) {
    obj_msg__msg__BinaryMap__fini(msg);
  }
  free(msg);
}


bool
obj_msg__msg__BinaryMap__Sequence__init(obj_msg__msg__BinaryMap__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  obj_msg__msg__BinaryMap * data = NULL;
  if (size) {
    data = (obj_msg__msg__BinaryMap *)calloc(size, sizeof(obj_msg__msg__BinaryMap));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = obj_msg__msg__BinaryMap__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        obj_msg__msg__BinaryMap__fini(&data[i - 1]);
      }
      free(data);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
obj_msg__msg__BinaryMap__Sequence__fini(obj_msg__msg__BinaryMap__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      obj_msg__msg__BinaryMap__fini(&array->data[i]);
    }
    free(array->data);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

obj_msg__msg__BinaryMap__Sequence *
obj_msg__msg__BinaryMap__Sequence__create(size_t size)
{
  obj_msg__msg__BinaryMap__Sequence * array = (obj_msg__msg__BinaryMap__Sequence *)malloc(sizeof(obj_msg__msg__BinaryMap__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = obj_msg__msg__BinaryMap__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
obj_msg__msg__BinaryMap__Sequence__destroy(obj_msg__msg__BinaryMap__Sequence * array)
{
  if (array) {
    obj_msg__msg__BinaryMap__Sequence__fini(array);
  }
  free(array);
}

bool
obj_msg__msg__BinaryMap__Sequence__are_equal(const obj_msg__msg__BinaryMap__Sequence * lhs, const obj_msg__msg__BinaryMap__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!obj_msg__msg__BinaryMap__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
obj_msg__msg__BinaryMap__Sequence__copy(
  const obj_msg__msg__BinaryMap__Sequence * input,
  obj_msg__msg__BinaryMap__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(obj_msg__msg__BinaryMap);
    obj_msg__msg__BinaryMap * data =
      (obj_msg__msg__BinaryMap *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!obj_msg__msg__BinaryMap__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          obj_msg__msg__BinaryMap__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!obj_msg__msg__BinaryMap__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
