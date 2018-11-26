"""
 ----------------------------------------------------
  @Author: tsukasa
  @Affiliation: Waseda University
  @Email: rinsa@suou.waseda.jp
  @Date: 2018-11-20 16:02:46
  @Last Modified by:   Tsukasa Nozawa
  @Last Modified time: 2018-11-26 23:21:46
 ----------------------------------------------------

  Usage:
   python find_shortest_path.py argvs[1] argvs[2] argvs[3]...
  
   argvs[1]  :  3d object         -->   .obj
   argvs[2]  :  fp for argvs[1]   -->   .txt


  Options:
   xxx       :  ??????????   -->   !!!!!!!!!!



"""

print(__doc__)

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components, dijkstra
import obj_functions as of
import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import queue

argvs = sys.argv
    


def init(width, height):
  """ initialize """
  glClearColor(102.0 / 255.0, 102.0 / 255.0, 204.0 / 255.0, 1.0)
  glEnable(GL_DEPTH_TEST) # enable shading
  glEnable(GL_CULL_FACE)
  glCullFace(GL_BACK)

  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  ##set perspective
  gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)



def display():
  """ display """
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()
  ##set camera
  # gluLookAt(0.0, 0.25, -1.0, mean[0], mean[1], mean[2], 0.0, 1.0, 0.0)
  gluLookAt(0.0, 5.0, 0.0, mean[0], mean[1], mean[2], 0.0, 0.0, 1.0)

  light0p = [ 0.0, 4.0, 0.0, 1.0 ]
  glLight(GL_LIGHT0, GL_POSITION, light0p)
  draw_obj()
  glFlush() 

def reshape(width, height):
  """callback function resize window"""
  glViewport(0, 0, width, height)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)


def draw_obj():

  glEnable(GL_LIGHTING)
  glEnable(GL_LIGHT0)


  for i in range(tri.shape[0]):
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 1.0)
    ver0 = ver[tri[i][0]] #* scale
    ver1 = ver[tri[i][1]] #* scale
    ver2 = ver[tri[i][2]] #* scale

    glNormal3f(fn[i][0], fn[i][1], fn[i][2])
    glVertex3f(ver0[0],ver0[1],ver0[2])
    glVertex3f(ver1[0],ver1[1],ver1[2])
    glVertex3f(ver2[0],ver2[1],ver2[2])

    glEnd()



  glDisable(GL_LIGHTING)
  glDisable(GL_LIGHT0)

  for i in range(tri.shape[0]):
    glLineWidth(5.0)
    glBegin(GL_LINE_LOOP)
    glColor3f(0.0, 0.0, 0.0)
    ver0 = ver[tri[i][0]] #* scale
    ver1 = ver[tri[i][1]] #* scale
    ver2 = ver[tri[i][2]] #* scale

    glNormal3f(fn[i][0], fn[i][1], fn[i][2])
    glVertex3f(ver0[0],ver0[1],ver0[2])
    glVertex3f(ver1[0],ver1[1],ver1[2])
    glVertex3f(ver2[0],ver2[1],ver2[2])

    glEnd()


  glLineWidth(20.0)
  glBegin(GL_LINE_LOOP)
  glColor3f(1.0, 0.0, 0.0)
  
  for p in shortest_path:
    ver0 = ver[p] #* scale

    glNormal3f(vn[p][0], vn[p][1], vn[p][2])
    glVertex3f(ver0[0],ver0[1],ver0[2])

  glEnd()


  glPointSize(30.0)
  glBegin(GL_POINTS)
  glColor3f(0.0, 0.0, 1.0)
  
  for p in landmark:
    ver0 = ver[p] #* scale
    glNormal3f(vn[p][0], vn[p][1], vn[p][2])
    glVertex3f(ver0[0],ver0[1],ver0[2])

  glEnd()


def calcu_weight(ver, tri):

  row = []
  col = []
  wgt = []

  for i in range(tri.shape[0]):
    a = tri[i][0]
    b = tri[i][1]
    c = tri[i][2]

    # edge 1
    w1 = np.linalg.norm(ver[b] - ver[a])
    row.append(a)
    col.append(b)
    wgt.append(w1)

    # edge 2
    w2 = np.linalg.norm(ver[c] - ver[b])
    row.append(b)
    col.append(c)
    wgt.append(w2)

    # edge 3
    w3 = np.linalg.norm(ver[a] - ver[c])
    row.append(c)
    col.append(a)
    wgt.append(w3)

  return np.array(row, dtype=np.int), np.array(col, dtype=np.int), np.array(wgt, dtype=np.float32)
  # return row, col, wgt


def calcu_normqal(ver, tri):

  vn = ver.copy()
  fn = []

  for i in range(tri.shape[0]):

    ab = ver[tri[i][1]] - ver[tri[i][0]]
    ac = ver[tri[i][2]] - ver[tri[i][0]]

    n = np.cross(ab, ac)
    n = n / np.linalg.norm(n)
    fn.append( n )

    vn[tri[i][0]] = n
    vn[tri[i][1]] = n
    vn[tri[i][2]] = n

  return np.array(vn, dtype=np.float), np.array(fn, dtype=np.float)




def load_landmark(path):

  landmark = []

  with open(path, 'r') as f:
    
    for line in f:
      pieces = line.split(' ')
      landmark.append(pieces[0])

  return np.array(landmark, dtype=np.int)



def write_shortest_path(filepath, shortest_path):

  with open(filepath, "w") as f:
    
    for i in range(shortest_path.shape[0]):
      if(i == shortest_path.shape[0]-1):
        f.write("{}".format(shortest_path[i]))
      else:
        f.write("{}\n".format(shortest_path[i]))



def find_shortest_path(ver, graph, landmark):
  
  # define start and goal
  shortest_path = []
  for i in range(landmark.shape[0]):

    if(i+1 == landmark.shape[0]):
      start = int(landmark[i])
      goal = int(landmark[0])
    else:
      start = int(landmark[i])
      goal = int(landmark[i+1])


    # find shortest-path
    # see here 
    # --> https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.sparse.csgraph.dijkstra.html
    dist_matrix, predecessors = dijkstra(graph, indices=start, return_predecessors=True)


    # create shortest-path index list
    path = [goal]
    prev = predecessors[goal]
    path.append(prev)
    for i in range(ver.shape[0]):

      if(prev == start):
        break
      else:
        prev = predecessors[prev]
        path.append(prev)

    path = path[::-1]
    shortest_path.extend(path[:-1])

  
  print("shortest-path index: {}".format(shortest_path))
  return np.array(shortest_path, dtype=np.int)


'''

section 1: shortest path

'''



def main():

  ######################
  # 1. load obj
  ######################
  ver, tri = of.loadobj(argvs[1])
  vn, fn = calcu_normqal(ver, tri)
  mean = np.mean(ver, axis=0)

  print("input vertex of shape: {}".format(ver.shape))
  print("input triangles of shape: {}".format(tri.shape))
  print("input vertex normal of shape: {}".format(vn.shape))
  print("input face normal of shape: {}".format(fn.shape))
  print("mean vertex of shape: {}".format(mean))



  ######################
  # 2. load landmark list
  ######################
  landmark = load_landmark(argvs[2])
  print("input landmark list: {}".format(landmark))




  ######################
  # 3. apply dijkstra for shortest path
  ######################

  # create sparse matrix
  row, col, wgt = calcu_weight(ver, tri)
  graph = csr_matrix((wgt, (row, col)), shape=(ver.shape[0], ver.shape[0]))


  # create sparse matrix
  # n_components, labels = connected_components(graph, directed=False)
  # print (n_components, labels)


  # search shortest path
  shortest_path = find_shortest_path(ver, graph, landmark)


  # save shortest-path as text fila
  dirname = os.path.dirname(argvs[1])
  basename = os.path.basename(argvs[1])[:-4]
  basename_landmark = os.path.basename(argvs[2])[:-4]
  # write_shortest_path(dirname+"/"+basename+"_"+basename_landmark+"_sp.txt", shortest_path)



  ######################
  # Option. visualize apth
  ######################
  glutInit(sys.argv)
  glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
  glutInitWindowSize(800, 800)     # window size
  glutInitWindowPosition(100, 100) # window position
  glutCreateWindow(b"test")      # show window
  glutDisplayFunc(display)         # draw callback function
  glutReshapeFunc(reshape)         # resize callback function
  init(300, 300)
  glutMainLoop()




#######################
# normal
#######################
# main()






#######################
# with OpenGL
#######################

# # 1. load obj
# ver, tri = of.loadobj(argvs[1])
# vn, fn = calcu_normqal(ver, tri)
# mean = np.mean(ver, axis=0)



# # 2. load landmark list

# landmark = load_landmark(argvs[2])



# # 3. apply dijkstra for shortest path



# # 4. create sparse matrix and search shortest path
# row, col, wgt = calcu_weight(ver, tri)
# graph = csr_matrix((wgt, (row, col)), shape=(ver.shape[0], ver.shape[0]))
# shortest_path = find_shortest_path(ver, graph, landmark)



# # 5. save shortest-path as text fila
# # dirname = os.path.dirname(argvs[1])
# # basename = os.path.basename(argvs[1])[:-4]
# # basename_landmark = os.path.basename(argvs[2])[:-4]
# # write_shortest_path(dirname+"/"+basename+"_"+basename_landmark+"_sp.txt", shortest_path)




# # 6. Option. visualize apth
# glutInit(sys.argv)
# glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
# glutInitWindowSize(800, 800)     # window size
# glutInitWindowPosition(100, 100) # window position
# glutCreateWindow(b"test")      # show window
# glutDisplayFunc(display)         # draw callback function
# glutReshapeFunc(reshape)         # resize callback function
# init(300, 300)
# glutMainLoop()
