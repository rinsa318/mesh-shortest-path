"""
 ----------------------------------------------------
  @Author: tsukasa
  @Affiliation: Waseda University
  @Email: rinsa@suou.waseda.jp
  @Date: 2018-11-26 17:57:15
  @Last Modified by:   tsukasa
  @Last Modified time: 2018-11-26 18:26:03
 ----------------------------------------------------

  Usage:
   python main.py argvs[1] argvs[2] argvs[3]...
  
   argvs[1]  :  ??????????   -->   !!!!!!!!!!
   argvs[2]  :  ??????????   -->   !!!!!!!!!!
   argvs[3]  :  ??????????   -->   !!!!!!!!!!
 
  Options:
   xxx       :  ??????????   -->   !!!!!!!!!!



"""


print(__doc__)

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
import sys
import numpy as np
# from OpenGL.GL import *
# from OpenGL.GLU import *
# from OpenGL.GLUT import *
import queue
import os


import obj_functions as of
import find_shortest_path as sp
import get_inside as gi 

argvs = sys.argv




def load_landmark(path):

  landmark = []

  with open(path, 'r') as f:
    
    for line in f:
      pieces = line.split(' ')
      landmark.append(pieces[0])

  return np.array(landmark, dtype=np.int)





######################
# 1. load obj
######################
ver, tri = of.loadobj(argvs[1])
# vn, fn = calcu_normqal(ver, tri)
mean = np.mean(ver, axis=0)

print("input vertex of shape: {}".format(ver.shape))
print("input triangles of shape: {}".format(tri.shape))
# print("input vertex normal of shape: {}".format(vn.shape))
# print("input face normal of shape: {}".format(fn.shape))
print("mean vertex of shape: {}".format(mean))



######################
# 2. load landmark list
######################
landmark = load_landmark(argvs[2])
print("input landmark list: {}".format(landmark))



######################
# 3. create graph from sparse matrix
######################
row, col, wgt = sp.calcu_weight(ver, tri)
graph = csr_matrix((wgt, (row, col)), shape=(ver.shape[0], ver.shape[0]))



######################
# 4. apply dijkstra for shortest path
######################
shortest_path = sp.find_shortest_path(ver, graph, landmark)




######################
# 5. find inside vertex within
######################
inner_face = gi.get_inside(ver, tri, graph, shortest_path)



######################
# 5. save
######################
dirname = os.path.dirname(argvs[1])
# basename = os.path.basename(argvs[1])[:-4]
basename_fp = os.path.basename(argvs[2])[:-4]
new_dir_path = dirname + "/" + basename_fp
if not os.path.exists(new_dir_path):
  os.mkdir(new_dir_path)

sp.write_shortest_path(new_dir_path + "/shortest-path.txt", shortest_path)
of.writeobj(new_dir_path+"/inside.obj", ver, inner_face)