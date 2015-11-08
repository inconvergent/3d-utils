# -*- coding: utf-8 -*-

def load(fn):

  from codecs import open
  from numpy import row_stack

  vertices = []
  faces = []

  with open(fn, 'r', encoding='utf8') as f:

    for l in f:
      if l.startswith('#'):
        continue

      values = l.split()
      if not values:
        continue
      if values[0] == 'v':
        vertices.append([float(v) for v in values[1:]])

      if values[0] == 'f':
        face = [int(v.split('//')[0])-1 for v in values[1:]]
        faces.append(face)

  try:
    faces = row_stack(faces)
  except ValueError:
    faces = None

  return {
    'faces': faces,
    'vertices': row_stack(vertices)
  }

def load_move_scale(
  fn,
  s=1,
  mx=[0,0,0]
):

  data = load(fn)

  vertices = data['vertices']
  faces = data['faces']

  xmax = vertices[:,0].max()
  xmin = vertices[:,0].min()
  ymax = vertices[:,1].max()
  ymin = vertices[:,1].min()
  zmax = vertices[:,2].max()
  zmin = vertices[:,2].min()
  dx = xmax - xmin
  dy = ymax - ymin
  dz = zmax - zmin

  print('original')
  print('x min max, {:0.8f} {:0.8f}, dst: {:0.8f}'.format(xmin,xmax,dx))
  print('y min max, {:0.8f} {:0.8f}, dst: {:0.8f}'.format(ymin,ymax,dy))
  print('z min max, {:0.8f} {:0.8f}, dst: {:0.8f}'.format(zmin,zmax,dz))

  vertices /= max([dx,dy,dz])

  vertices[:,0] *= s
  vertices[:,1] *= s
  vertices[:,2] *= s

  vertices[:,0] += mx[0]
  vertices[:,1] += mx[1]
  vertices[:,2] += mx[2]

  xmax = vertices[:,0].max()
  xmin = vertices[:,0].min()
  ymax = vertices[:,1].max()
  ymin = vertices[:,1].min()
  zmax = vertices[:,2].max()
  zmin = vertices[:,2].min()
  dx = xmax - xmin
  dy = ymax - ymin
  dz = zmax - zmin

  print('rescaled')
  print('x min max, {:0.8f} {:0.8f}, dst: {:0.8f}'.format(xmin,xmax,dx))
  print('y min max, {:0.8f} {:0.8f}, dst: {:0.8f}'.format(ymin,ymax,dy))
  print('z min max, {:0.8f} {:0.8f}, dst: {:0.8f}'.format(zmin,zmax,dz))

  return {
    'faces': faces,
    'vertices': vertices
  }

def export(obj_name, fn, verts, tris=None, meta=False):

  from codecs import open

  vnum = len(verts)

  if tris is not None:
    fnum = len(tris)
  else:
    fnum = 0

  print('storing mesh ...')
  print('num vertices: {:d}, num triangles: {:d}'.format(vnum, fnum))

  with open(fn, 'wb', encoding='utf8') as f:

    if meta:
      f.write('# meta:\n')
      f.write(meta+'\n')

    f.write('# info:\n')

    f.write('# vnum: {:d}\n# fnum: {:d}\n\n\n'
      .format(vnum, fnum))

    f.write('o {:s}\n'.format(obj_name))

    for v in verts:
      f.write('v {:f} {:f} {:f}\n'.format(*v))

    f.write('s off\n')

    if tris is not None:
      for t in tris:
        t += 1
        f.write('f {:d} {:d} {:d}\n'.format(*t))

    print('done.')

