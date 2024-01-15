// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from obj_msg:msg/Objlst.idl
// generated code does not contain a copyright notice
#include "obj_msg/msg/detail/objlst__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>


// Include directives for member types
// Member `objects`
#include "obj_msg/msg/detail/obj__functions.h"

bool
obj_msg__msg__Objlst__init(obj_msg__msg__Objlst * msg)
{
  if (!msg) {
    return false;
  }
  // w
  // h
  // objects
  if (!obj_msg__msg__Obj__Sequence__init(&msg->objects, 0)) {
    obj_msg__msg__Objlst__fini(msg);
    return false;
  }
  return true;
}

void
obj_msg__msg__Objlst__fini(obj_msg__msg__Objlst * msg)
{
  if (!msg) {
    return;
  }
  // w
  // h
  // objects
  obj_msg__msg__Obj__Sequence__fini(&msg->objects);
}

bool
obj_msg__msg__Objlst__are_equal(const obj_msg__msg__Objlst * lhs, const obj_msg__msg__Objlst * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // w
  if (lhs->w != rhs->w) {
    return false;
  }
  // h
  if (lhs->h != rhs->h) {
    return false;
  }
  // objects
  if (!obj_msg__msg__Obj__Sequence__are_equal(
      &(lhs->objects), &(rhs->objects)))
  {
    return false;
  }
  return true;
}

bool
obj_msg__msg__Objlst__copy(
  const obj_msg__msg__Objlst * input,
  obj_msg__msg__Objlst * output)
{
  if (!input || !output) {
    return false;
  }
  // w
  output->w = input->w;
  // h
  output->h = input->h;
  // objects
  if (!obj_msg__msg__Obj__Sequence__copy(
      &(input->objects), &(output->objects)))
  {
    return false;
  }
  return true;
}

obj_msg__msg__Objlst *
obj_msg__msg__Objlst__create()
{
  obj_msg__msg__Objlst * msg = (obj_msg__msg__Objlst *)malloc(sizeof(obj_msg__msg__Objlst));
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(obj_msg__msg__Objlst));
  bool success = obj_msg__msg__Objlst__init(msg);
  if (!success) {
    free(msg);
    return NULL;
  }
  return msg;
}

void
obj_msg__msg__Objlst__destroy(obj_msg__msg__Objlst * msg)
{
  if (msg) {
    obj_msg__msg__Objlst__fini(msg);
  }
  free(msg);
}


bool
obj_msg__msg__Objlst__Sequence__init(obj_msg__msg__Objlst__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  obj_msg__msg__Objlst * data = NULL;
  if (size) {
    data = (obj_msg__msg__Objlst *)calloc(size, sizeof(obj_msg__msg__Objlst));
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = obj_msg__msg__Objlst__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        obj_msg__msg__Objlst__fini(&data[i - 1]);
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
obj_msg__msg__Objlst__Sequence__fini(obj_msg__msg__Objlst__Sequence * array)
{
  if (!array) {
    return;
  }
  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      obj_msg__msg__Objlst__fini(&array->data[i]);
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

obj_msg__msg__Objlst__Sequence *
obj_msg__msg__Objlst__Sequence__create(size_t size)
{
  obj_msg__msg__Objlst__Sequence * array = (obj_msg__msg__Objlst__Sequence *)malloc(sizeof(obj_msg__msg__Objlst__Sequence));
  if (!array) {
    return NULL;
  }
  bool success = obj_msg__msg__Objlst__Sequence__init(array, size);
  if (!success) {
    free(array);
    return NULL;
  }
  return array;
}

void
obj_msg__msg__Objlst__Sequence__destroy(obj_msg__msg__Objlst__Sequence * array)
{
  if (array) {
    obj_msg__msg__Objlst__Sequence__fini(array);
  }
  free(array);
}

bool
obj_msg__msg__Objlst__Sequence__are_equal(const obj_msg__msg__Objlst__Sequence * lhs, const obj_msg__msg__Objlst__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!obj_msg__msg__Objlst__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
obj_msg__msg__Objlst__Sequence__copy(
  const obj_msg__msg__Objlst__Sequence * input,
  obj_msg__msg__Objlst__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(obj_msg__msg__Objlst);
    obj_msg__msg__Objlst * data =
      (obj_msg__msg__Objlst *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!obj_msg__msg__Objlst__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          obj_msg__msg__Objlst__fini(&data[i]);
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
    if (!obj_msg__msg__Objlst__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
