"""
 ----------------------------------------------------
  @Author: tsukasa
  @Affiliation: Waseda University
  @Email: rinsa@suou.waseda.jp
  @Date: 2018-11-20 16:56:02
  @Last Modified by:   tsukasa
  @Last Modified time: 2018-11-26 18:27:10
 ----------------------------------------------------

  Usage:
   python get_inside.py argvs[1] argvs[2] argvs[3]...
  
   argvs[1]  :  ??????????   -->   !!!!!!!!!!
   argvs[2]  :  ??????????   -->   !!!!!!!!!!
   argvs[3]  :  ??????????   -->   !!!!!!!!!!
 
  Options:
   xxx       :  ??????????   -->   !!!!!!!!!!



"""



import obj_functions as of
import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


import queue
from scipy.sparse import *
from scipy import sparse



def load_landmark(path):

  landmark = []

  with open(path, 'r') as f:
    
    for line in f:
      pieces = line.split(' ')
      landmark.append(pieces[0])

  return np.array(landmark, dtype=np.int)





def calcu_edge_weight(ver, tri):

  row = []
  col = []
  wgt = []
  # w = []

  
  for i in range(tri.shape[0]):
    a = tri[i][0]
    b = tri[i][1]
    c = tri[i][2]

    # edge 1
    # w1 = np.linalg.norm(ver[b] - ver[a])
    # if(not(w1 in w)):
    # w.append(w1)
    row.append(a)
    col.append(b)
    wgt.append(1)

    # edge 2
    # w2 = np.linalg.norm(ver[c] - ver[b])
    # if(not(w2 in w)):
    # w.append(w2)
    row.append(b)
    col.append(c)
    wgt.append(1)

    # edge 3
    # w3 = np.linalg.norm(ver[a] - ver[c])
    # if(not(w3 in w)):
    # w.append(w3)
    row.append(c)
    col.append(a)
    wgt.append(1)

  # print(len(row))
  # print(w)

  return np.array(row, dtype=np.int), np.array(col, dtype=np.int), np.array(wgt, dtype=np.float32)
  # return row, col, wgt




def get_inside(ver, tri, graph, shortest_path):



  # 1. calc mean vertex within shportest-path
  mean_sp = np.zeros((3,), dtype=np.float)
  for i in shortest_path:
    mean_sp += ver[i]

  mean_sp = mean_sp / shortest_path.shape[0]
  print("mean of sp list: {}".format(mean_sp))



  # 2. define closest point from mean_sp as init vertex
  dif = np.linalg.norm(ver-mean_sp, axis=1)
  init_index = np.argmin(dif)
  print("init index: {}".format(init_index))

  # # create node by using sparse matrix
  # row, col, wgt = calcu_edge_weight(ver, tri)
  # graph = csr_matrix((wgt, (row, col)), shape=(ver.shape[0], ver.shape[0]))

 

  # 3. get node information
  # see here --> http://hamukazu.com/2014/12/03/internal-data-structure-scipy-sparse/
  weight = graph.data
  indices = graph.indices
  indptr = graph.indptr



  # 4. initialize queue
  q = queue.Queue()
  inner_vertex = []
  temp = [init_index]
  q.put(init_index)



  # 5. stsrt search
  while True:

    temp = list(set(temp))
    print("current queue size: {}".format(q.qsize()))
    print(len(inner_vertex+ shortest_path.tolist()))
    
    if q.empty():
      print("done!")
      break

    else:
      i = q.get()
      inner_vertex.append(i)

      # index = np.any(np.array(tri) == i, axis=1)
      # index_num = np.where(np.any(tri == i, axis=1) == 1)[0]
      # temp_face.extend(index_num)
      # print(index_num)

      edge = indices[indptr[i]:indptr[i+1]]
      for item in edge:

        if(np.any(shortest_path == item)):
          continue

        elif(np.any(np.array(temp) == item)):
          continue
        
        else:
          q.put(item)
          temp.append(item)


  inner_ver_index = inner_vertex + shortest_path.tolist()
  print("inner mesh vertex number is: {}".format(len(inner_ver_index)))






  # inside points index to xyz value 
  # point = []
  # for i in inner_ver_index:
  #   point.append(ver[i])

  # point = np.array(point, dtype=np.float32)
  # of.writepoint("test-cut-point2.obj", point)


  # 6. find face index for index points
  new_face_index = []
  count = 1
  for i in inner_vertex:
    print("{} / {}".format(count, len(inner_vertex)))

    new_face_index += np.where(np.any(tri == i, axis=1) == 1)[0].tolist()
    count += 1

  new_face_index = list(set(new_face_index))




  # 7. extract face component
  inner_face = []
  count = 1
  for tf in new_face_index:

    print("{} / {}".format(count, len(new_face_index)))
    inner_face.append( tri[tf] )
    count += 1 

  # inner_face = np.array(inner_face, dtype=np.int)
  # of.writeobj("test-cut-test2.obj", ver, inner_face)


  return np.array(inner_face, dtype=np.int)




def main():

  ######################
  # 1. load obj
  ######################
  argvs = sys.argv
  ver, tri = of.loadobj(argvs[1])




  ######################
  # 2. load shortest-path index list
  ######################
  sp = load_landmark(argvs[2])




  ######################
  # 3. find inside vertex within
  ######################
  # create node by using sparse matrix
  row, col, wgt = calcu_edge_weight(ver, tri)
  graph = csr_matrix((wgt, (row, col)), shape=(ver.shape[0], ver.shape[0]))


  inner_face = get_inside(ver, tri, graph, sp)
  print(inner_face)



  ######################
  # 5. save as obj
  ######################
  dirname = os.path.dirname(argvs[1])
  basename = os.path.basename(argvs[1])[:-4]
  basename_fp = os.path.basename(argvs[2])[:-4]
  # write_shortest_path(dirname+"/"+basename+"_"+basename_fp+"_sp.txt", shortest_path)
  of.writeobj(dirname+"/"+basename+"_"+basename_fp+".obj", ver, inner_face)




# main()