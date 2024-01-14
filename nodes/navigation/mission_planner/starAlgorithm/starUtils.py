from cmath import inf
from turtle import pos
import numpy as np
import math
import time
from pqdict import pqdict

#returns desired heuristic given current position and target position
def heuristic(curr_pos, targetpos):
    return np.linalg.norm(curr_pos-targetpos)
    #return 2*max(np.abs(curr_pos-targetpos))

#returns a set of arrays between a center point and an end point
def bresenham2D_array(sx, sy, ex, ey):
  '''
  Bresenham's ray tracing algorithm in 2D.
  Inputs:
	  (sx, sy)	start point of ray
	  (ex, ey)	end point of ray
  '''
  sx = int(np.round(sx))
  sy = int(np.round(sy))
  ex = (np.round(ex)).astype(int)
  ey = (np.round(ey)).astype(int)
  dx = abs(ex-sx)
  dy = abs(ey-sy)
  steep = abs(dy)>abs(dx)

  
  dx[steep],dy[steep] = dy[steep],dx[steep] # swap 
  dy = -dy
  final_x = []
  final_y = []
  half_difference = np.floor(dx/2)
  more_equation = dy*dx+half_difference-1

  for i in range(len(dy)):
    if dy[i] == 0:
      q = np.zeros((dx[i]+1,1))
    else:
      q = np.append(0,np.greater_equal(np.diff(np.mod(np.arange(half_difference[i], more_equation[i],dy[i]),dx[i])),0))
    if steep[i]:
      if sy <= ey[i]:
        y = np.arange(sy,ey[i]+1)
      else:
        y = np.arange(sy,ey[i]-1,-1)
      if sx <= ex[i]:
        x = sx + np.cumsum(q)
      else:
        x = sx - np.cumsum(q)
    else:
      if sx <= ex[i]:
        x = np.arange(sx,ex[i]+1)
      else:
        x = np.arange(sx,ex[i]-1,-1)
      if sy <= ey[i]:
        y = sy + np.cumsum(q)
      else:
        y = sy - np.cumsum(q)
    final_x.append(x)
    final_y.append(y)
  return final_y,final_x

def bresenham2D(sx, sy, ex, ey):
  '''
  Bresenham's ray tracing algorithm in 2D.
  Inputs:
	  (sx, sy)	start point of ray
	  (ex, ey)	end point of ray
  '''
  sx = int(round(sx))
  sy = int(round(sy))
  ex = int(round(ex))
  ey = int(round(ey))
  dx = abs(ex-sx)
  dy = abs(ey-sy)
  steep = abs(dy)>abs(dx)
  if steep:
    dx,dy = dy,dx # swap 

  if dy == 0:
    q = np.zeros((dx+1,1))
  else:
    q = np.append(0,np.greater_equal(np.diff(np.mod(np.arange( np.floor(dx/2), -dy*dx+np.floor(dx/2)-1,-dy),dx)),0))
  if steep:
    if sy <= ey:
      y = np.arange(sy,ey+1)
    else:
      y = np.arange(sy,ey-1,-1)
    if sx <= ex:
      x = sx + np.cumsum(q)
    else:
      x = sx - np.cumsum(q)
  else:
    if sx <= ex:
      x = np.arange(sx,ex+1)
    else:
      x = np.arange(sx,ex-1,-1)
    if sy <= ey:
      y = sy + np.cumsum(q)
    else:
      y = sy - np.cumsum(q)
  return np.vstack((x,y))

def all_children(envmap, robotpos):
    numofdirs = 8
    dX = [-1, -1, -1, 0, 0, 1, 1, 1]
    dY = [-1,  0,  1, -1, 1, -1, 0, 1]
    dirArray = []

    for dd in range(numofdirs):
        newx = robotpos[0] + dX[dd]
        newy = robotpos[1] + dY[dd]
        if (newx >= 0 and newx < envmap.shape[0] and newy >= 0 and newy < envmap.shape[1]):
            if(envmap[newx, newy] == 0):
                dirArray.append(np.array((newx,newy)))
    return dirArray

def ocupied_children(envmap, robotpos):
    numofdirs = 8
    dX = [-1, -1, -1, 0, 0, 1, 1, 1]
    dY = [-1,  0,  1, -1, 1, -1, 0, 1]
    dirArray = []

    for dd in range(numofdirs):
        newx = robotpos[0] + dX[dd]
        newy = robotpos[1] + dY[dd]
        if (newx >= 0 and newx < envmap.shape[0] and newy >= 0 and newy < envmap.shape[1]):
            if(envmap[newx, newy] == 1):
                dirArray.append(np.array((newx,newy)))
    return dirArray
#stores the g, v, and heuristic values of a position, as well as the path that took it's lowest g value
class stateObject():
    def __init__(self, position, target, previousPosition = -1):
        self.position = tuple(position)
        self.previousPosition = previousPosition

        if previousPosition == -1:
            self.g = 0
        else:
            self.g = previousPosition.g+1
        
        self.h = heuristic(position,target)
        self.f = self.g+ self.h

    def updateG(self, newG):
        self.g = newG
        self.f = self.g+ self.h

    #overloading operators
    def __gt__(self, other):
        return self.f > other.f
    
    def __lt__(self, other):
        return self.f < other.f

    def __ge__(self, other):
        return self.f >= other.f
    
    def __le__(self, other):
        return self.f <= other.f

#stores the g, v, heuristic, and keys for D* values of a position, as well as the path that took it's lowest g value
class stateObjectD():
    def __init__(self, position, target, previousPosition = -1):
        self.position = tuple(position)
        self.previousPosition = previousPosition

        if previousPosition == -1:
            self.g = 0
        else:
            self.g = previousPosition.g+1

        self.h = heuristic(position,target)
        self.v = inf
        self.f = self.g+self.h
        self.key = [min(self.g,self.v)+ self.h, min(self.g,self.v)]

    def updateG(self, newG, target):
        self.g = newG
        self.f = self.g+ self.h
        self.h = heuristic(self.position,target)
        self.key = [min(self.g,self.v)+ self.h, min(self.g,self.v)]

    #overloading operators
    def __gt__(self, other):
        if self.key[0] != other.key[0]:
            return self.key[0] > other.key[0]
        return self.key[1] > other.key[1]
    
    def __lt__(self, other):
        if self.key[0] != other.key[0]:
            return self.key[0] < other.key[0]
        return self.key[1] < other.key[1]

    def __ge__(self, other):
        if self.key[0] != other.key[0]:
            return self.key[0] >= other.key[0]
        return self.key[1] >= other.key[1]   

    def __le__(self, other):
        if self.key[0] != other.key[0]:
            return self.key[0] <= other.key[0]
        return self.key[1] <= other.key[1]

#stores the current g, h, f and possible children of a node
class stateObjectRPM():
    def __init__(self, position, target):
        self.position = tuple(position)
        self.previousPosition = -1

        self.g = inf
        
        self.h = heuristic(position,target)
        self.f = self.g+ self.h

        self.children = pqdict({})

    def updateG(self, newG):
        self.g = newG
        self.f = self.g+ self.h

    #overloading operators
    def __gt__(self, other):
        return self.f > other.f
    
    def __lt__(self, other):
        return self.f < other.f

    def __ge__(self, other):
        return self.f >= other.f
    
    def __le__(self, other):
        return self.f <= other.f