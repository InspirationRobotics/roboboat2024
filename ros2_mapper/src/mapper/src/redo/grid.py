
def mk_grid(w, h):
    grid = []

    for i in range(0, w):
        grid.append([])

    for i in range(0, w):
        for j in range(0, h):
            grid[i].append([])
        
    return grid


def mk_obj(type, id, mission, pose, ts):
    o = {
        "type": type,
        "id": id,
        "mission": mission,
        "pose": pose,
        "times_seen": ts,
    }
    
    return o

def add_obj(grid, obj):
    j = 0

    x = int((len(grid) - 1) / 2)
    y = int((len(grid[0]) - 1) / 2)

    x += int(obj.get('pose')[0])
    y += int(obj.get('pose')[1])
    
    for i in grid[x][y]:
        if i.get('type') == obj.get('type'):
            grid[x][y][j]["times_seen"] += 1
            j += 1
            return
        
    grid[x][y].append(mk_obj(obj.get('type'), obj.get('id'), obj.get('mission'), obj.get('pose'), 1))


def get_objs_by_type(grid, o_type):

    objs = []
    for row in grid:
        for col in row:
            for obj in col:
                if obj.get('type') == o_type:
                    objs.append(obj)

    return objs


def get_most_freq_objs(grid, o_type, n):

    objs = get_objs_by_type(grid, o_type)
    print(objs)

    freq_objs = []

    for i in range(0, n):
        o = mk_obj("buoy", "nil", "nil", [[], []], 0)
        
        for j in range(0, len(objs)):
            if objs[j].get("times_seen") > o.get("times_seen"):
                o = objs[j]
                
        if o.get('pose') == [[], []]:
            return freq_objs

        freq_objs.append(o)
        print(freq_objs)
        objs.remove(o)

    return freq_objs


def classify_gate_objs(grid):

    left = get_most_freq_objs(grid, "redbuoy", 2)
    right = get_most_freq_objs(grid, "greenbuoy", 2)

    if (len(left) == 2):
        if left[0].get('pose')[1] > left[1].get('pose')[1]:
            left[0]['id'] = "lb"
            left[1]['id'] = "lf"
        else:
            left[0]['id'] = "lf"
            left[1]['id'] = "lb"
    elif (len(left) == 1):
        left[0]['id'] = "lf|lb"

    if (len(right) == 2):
        if right[0].get('pose')[1] > right[1].get('pose')[1]:
            right[0]['id'] = "rb"
            right[1]['id'] = "rf"
        else:
            right[0]['id'] = "rf"
            right[1]['id'] = "rb"
    elif (len(right) == 1):
        right[0]['id'] = "rf|rb"
            
            
    objs = []
    for i in left:
        objs.append(i)
    for i in right:
        objs.append(i)

    return objs


