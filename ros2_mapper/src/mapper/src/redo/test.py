from grid import *

grid = mk_grid(12, 12)
lf = mk_obj("redbuoy", "nil", "nil", [0, 0], 0)
lb = mk_obj("redbuoy", "nil", "nil", [0, 4], 0)
rf = mk_obj("greenbuoy", "nil", "nil", [4, 0], 0)
rb = mk_obj("greenbuoy", "nil", "nil", [4, 4], 0)

add_obj(grid, lf)
add_obj(grid, lf)
add_obj(grid, lb)
add_obj(grid, rb)
add_obj(grid, rf)
add_obj(grid, rb)
add_obj(grid, rf)

print(classify_gate_objs(grid))
