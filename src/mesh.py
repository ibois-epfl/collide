import trimesh as tm
import open3d as o3d

import logging
logger = logging.getLogger('root')

class MeshContainer:
    def __init__(self, name, vertices=None, faces=None, path=None, trimesh=None):
        self._name = name
        self._vertices = vertices
        self._faces = faces

        self._path = path

        self._trimesh = None
        self._o3dmesh = None
        self._o3dlineset = None

        self._is_watertight = None

        self.is_colliding = False
        self.collisions = set()

    def load_trimesh(self, path : str) -> None:
        if path is not None:
            self.trimesh = tm.load(path)
            self.path = path
            if self.trimesh.is_watertight:
                self._vertices = self.trimesh.vertices
                self._faces = self.trimesh.faces
            else:
                logger.debug(f"[ERROR]: Mesh {self} in {self.path} is not watertight")
                exit(-1)
        else:
            raise ValueError("Path is None")

    def _cvt_trimesh2o3d(self, trimesh : tm.Trimesh) -> o3d.geometry.TriangleMesh:
        self.o3dmesh = trimesh.as_open3d
        return self.o3dmesh

    def _cvt_o3dmesh2linest(self, o3dmesh : o3d.geometry.TriangleMesh) -> o3d.geometry.LineSet:
        self.o3dlineset = o3d.geometry.LineSet.create_from_triangle_mesh(o3dmesh)
        return self.o3dlineset

    def __str__(self):
        return f"{self.name})"

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name : str):
        if isinstance(name, str):
            self._name = name
        else:
            self._name = None
    
    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, path : str):
        if isinstance(path, str):
            self._path = path
        else:
            self._path = None

    @property
    def trimesh(self):
        return self._trimesh

    @trimesh.setter
    def trimesh(self, trimesh):
        if isinstance(trimesh, tm.base.Trimesh):
            self._trimesh = trimesh
        else:
            raise TypeError("[ERROR]: No type trimesh.base.Trimesh")

    @property
    def o3dmesh(self):
        if self._o3dmesh is None:
            self._cvt_trimesh2o3d(self.trimesh)
        return self._o3dmesh
    
    @o3dmesh.setter
    def o3dmesh(self, value : o3d.geometry.TriangleMesh):
        if isinstance(value, o3d.geometry.TriangleMesh):
            self._o3dmesh = value
        else:
            raise TypeError("[ERROR]: No type open3d.geometry.TriangleMesh")

    @property
    def o3dlineset(self):
        if self._o3dlineset is None:
            self._cvt_o3dmesh2linest(self.o3dmesh)
        return self._o3dlineset
    
    @o3dlineset.setter
    def o3dlineset(self, value : o3d.geometry.LineSet):
        if isinstance(value, o3d.geometry.LineSet):
            self._o3dlineset = value
        else:
            raise TypeError("[ERROR]: No type open3d.geometry.LineSet")

    @property
    def is_watertight(self):
        if self._is_watertight is None:
            self._is_watertight = self.trimesh.is_watertight
        return self._is_watertight