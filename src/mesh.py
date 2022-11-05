import trimesh as tm


class MeshContainer:
    def __init__(self, name, vertices=None, faces=None, path=None):
        self._name = name
        self._vertices = vertices
        self._faces = faces

        self._path = path

        self._trimesh = None

        self.is_colliding = False
        self.collisions = set()

    def load_trimesh(self, path : str):
        if path is not None:
            self.trimesh = tm.load(path)
            if self.trimesh.is_watertight:
                self._vertices = self.trimesh.vertices
                self._faces = self.trimesh.faces
            else:
                raise Exception("Mesh is not watertight")
        else:
            raise ValueError("Path is None")
        self.path = path

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
            raise TypeError("No type trimesh.base.Trimesh")