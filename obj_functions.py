
import numpy as np
import sys
import os


def loadobj(path):
  vertices = []
  #texcoords = []
  triangles = []
  normals = []

  with open(path, 'r') as f:
    for line in f:
      if line[0] == '#':
        continue

      pieces = line.split(' ')

      if pieces[0] == 'v':
        #print pieces[1]
        # x = float(pieces[1])
        # y = float(pieces[2])
        # z = float(pieces[3])

        # if (rot == 180 and axis == 1):
        #   pieces[1] = -1.0 * x
        #   pieces[3] = -1.0 * z
        #   vertices.append([float(x) for x in pieces[1:4]])
        # elif (rot == -90 and axis == 0):
        #   pieces[2] = z
        #   pieces[3] = -1.0 * y
        #   vertices.append([float(x) for x in pieces[1:4]])
        # else:
        vertices.append([float(x) for x in pieces[1:4]])			
      # elif pieces[0] == 'vt':
      #   texcoords.append([float(x) for x in pieces[1:]])
      elif pieces[0] == 'f':
        if pieces[1] == '':
            triangles.append([int(x.split('/')[0]) - 1 for x in pieces[2:]])
        else: 
            triangles.append([int(x.split('/')[0]) - 1 for x in pieces[1:]])
      elif pieces[0] == 'vn':
        normals.append([float(x) for x in pieces[1:]])
      else:
        pass

  return (np.array(vertices, dtype=np.float32),
            #np.array(texcoords, dtype=np.float32),
            np.array(triangles, dtype=np.int32))#,
            # np.array(normals, dtype=np.float32))

def loadobj_with_segment_info(path):
  vertices = []
  #texcoords = []
  triangles = []
  # normals = []
  segment_triangles = []
  segment_labels = []
  segment_faces = []
  t_labels = [] 
  line_num = 0
  group = -1
  face_num = -1
  with open(path, 'r') as f:
    
    for line in f:
      line_num += 1

      if line[0] == '#':
        continue
      pieces = line.split(' ')

      if pieces[0] == 'v':
        vertices.append([float(x) for x in pieces[1:]])

      elif pieces[0] == 'f':
        if group > -1:
            face_num += 1
            if pieces[1] == '':
                triangles.append([int(x.split('/')[0]) - 1 for x in pieces[2:]])
                segment_triangles[group].append([int(x.split('/')[0]) - 1 for x in pieces[2:]])
                segment_faces[group].append(face_num)
                t_labels.append(segment_labels[group])
            else: 
                triangles.append([int(x.split('/')[0]) - 1 for x in pieces[1:]])
                segment_triangles[group].append([int(x.split('/')[0]) - 1 for x in pieces[1:]])
                segment_faces[group].append(face_num)
                t_labels.append(segment_labels[group])
      elif pieces[0] == 'usemtl':
        group += 1
        material_name = pieces[1].replace('\n', '')
        segment_triangles.append( [] )
        segment_faces.append([])
        segment_labels.append(material_name.rstrip())
      # elif pieces[0] == 'vn':
      #   normals.append([float(x) for x in pieces[1:]])
      else:
        pass
  #segment_triangles.append( ["end", line_num + 2] )

  return (np.array(vertices, dtype=np.float32),
            #np.array(texcoords, dtype=np.float32),
            np.array(triangles, dtype=np.int32),
            # np.array(normals, dtype=np.float32),
            segment_triangles, 
            segment_faces,
            segment_labels)

def writeobj(filepath, vertices, triangles):
  with open(filepath, "w") as f:
    for i in range(vertices.shape[0]):
      f.write("v {} {} {}\n".format(vertices[i, 0], vertices[i, 1], vertices[i, 2]))
    for i in range(triangles.shape[0]):
      f.write("f {} {} {}\n".format(triangles[i, 0] + 1, triangles[i, 1] + 1, triangles[i, 2] + 1))




def writepoint(filepath, vertices):
  with open(filepath, "w") as f:
    for i in range(vertices.shape[0]):
      f.write("v {} {} {}\n".format(vertices[i, 0], vertices[i, 1], vertices[i, 2]))
    # for i in range(triangles.shape[0]):
    #   f.write("f {} {} {}\n".format(triangles[i, 0] + 1, triangles[i, 1] + 1, triangles[i, 2] + 1))



