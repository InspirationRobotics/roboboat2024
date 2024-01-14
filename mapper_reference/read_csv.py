# to use the input.csv file as a data file to read user input
from floating_objects import Object_Colors, Object_Types, Floating_Object
import csv

#taking input from data file csv
def read_input(file_name):
    data = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                #skipping the header
                line_count += 1
            else:
                #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')

                dict = {"color": row[0], "lat": row[1], "long": row[2], "type": row[3]}
                data.append(dict)
                line_count += 1
        #print(f'Processed {line_count} lines.')
    return data

# lookup tables to convert from string to class object
def lookupcolor(color):
    if color == "RED":
        return Object_Colors.RED
    if color == "GREEN":
        return Object_Colors.GREEN
    if color == "WHITE":
        return Object_Colors.WHITE
    if color == "BLACK":
        return Object_Colors.BLACK

# lookup tables to convert from string to class object
def lookuptype(type):
    if type == "BOUY":
        return Object_Types.BOUY
    if type == "OBSTACLE":
        return Object_Types.OBSTACLE
    if type == "LIGHT_TOWER":
        return Object_Types.LIGHT_TOWER
    if type == "DRONE_LANDING_PAD":
        return Object_Types.DRONE_LANDING_PAD
    if type == "RACQUET_BALL_TARGET":
        return Object_Types.RACQUET_BALL_TARGET
    if type == "WILDLIFE_PLATYPUS":
        return Object_Types.WILDLIFE_PLATYPUS
    if type == "WILDLIFE_CROCODILE":
        return Object_Types.WILDLIFE_CROCODILE
    if type == "WILDLIFE_TURTLE":
        return Object_Types.WILDLIFE_TURTLE

# assemblying class objects based off string data
def format_data(data, grid):
    items = []
    for dict in data:
        color = lookupcolor(dict["color"])
        type = lookuptype(dict["type"])
        x,y = grid.gps_to_grid(float(dict["lat"]), float(dict["long"]))
        item  = Floating_Object(color,[x,y],type)
        items.append(item)
    return items

#data = read_input("input2.cvs")
#print(format_data(data))