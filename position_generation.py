from math import sin, cos, pi, atan2, degrees
import numpy as np
from functools import cmp_to_key

bond_length = 1
layer_distance = 2
scale = 60
increment = 4
n_layer = 5
dislocation_start = 20
dislocation_range_y = 5
dislocation_range_x = 19



dislocation_end = dislocation_start -dislocation_range_y +1
step = 1 /dislocation_range_y
v1 = np.array([1, 0, 0]) * bond_length
v2 = np.array([cos(pi*2/3), sin(pi*2/3), 0]) * bond_length
v3 = np.array([0, 0, 1]) * layer_distance
center = (dislocation_range_x +dislocation_start -1) *v1 +dislocation_start *v2
positions = []
range_j1 = 0
range_i1 = 0
range_i2 = scale -1

def cmp(a=np.array([1,2,3]),b=np.array([2,3,4])):
     if a[2] != b[2]:
          return a[2]-b[2]
     else:
          a1 = atan2(a[1]-center[1], a[0]-center[0])
          a2 = degrees(a1)
          b1 = atan2(b[1]-center[1], b[0]-center[0])
          b2 = degrees(b1)
          return a2 - b2


for k in range(n_layer):
     for i in range(range_i1, range_i2 +1):
          range_i2 = scale -increment *(k +1) -1
          for j in range(range_j1, i -range_i1 +range_j1 +1):
               w = v1*i+v2*j 
               if j >= dislocation_end and j <= dislocation_start and i <= dislocation_range_x +dislocation_start -1:
                    w = w + v3 * step * (dislocation_start -j +1) 
                    positions.append(w+v3*k)
               elif i <= range_i2 and j < dislocation_end:
                    positions.append(w+v3*(k+1))
               elif j >= dislocation_end:
                    positions.append(w+v3*k) 
     range_j1 = increment *(k+1)
     range_i1 = increment *(k+1) *2
for i in range(scale):
     for j in range(dislocation_end):
          w = v1*i+v2*j 
          if j >i:
               continue
          positions.append(w)

positions.sort(key = cmp_to_key(cmp))

with open('positions.xyz','w') as file:
     file.write('{}\n'.format(len(positions)))
     file.write('{}\n'.format('screw dislocation driven spiral'))
     for args in positions:
          file.write('  {}        {}        {}        {}\n'.format('S',*args)) 