#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from string import ascii_lowercase as alc
import os

import log
logger = log.setup_custom_logger('root')

import open3d as o3d
import trimesh as tm
from mesh import MeshContainer
import numpy as np
# import graphviz

from tqdm import tqdm
import util

CLR_ORANGE = [1, 0.706, 0]
CLR_LIGHT_GRAY = [0.8, 0.8, 0.8]
CLR_BLACK = [0, 0, 0]


def main() -> None:

    DATA_DIR : str = "./data/"
    OUT_DIR : str = "./out/"

    # ------------------------------------------------------------------->
    logger.debug(f"[INFO]: load meshes on memory files from container")
    mesh_dict : dict = {}
    a_i = 0
    for i,file in enumerate(os.listdir(DATA_DIR)):
        if file.endswith(".ply"):
            tmp_mesh = MeshContainer(alc[a_i])
            tmp_mesh.load_trimesh(DATA_DIR + file)
            mesh_dict[alc[a_i]] = tmp_mesh
            a_i += 1

    # ------------------------------------------------------------------->
    logger.debug(f"[INFO]: load meshes to collision manager")
    tm_CollManager : CollisionManager = tm.collision.CollisionManager()
    for mesh in mesh_dict.values():
        tm_CollManager.add_object(mesh.name, mesh.trimesh)

    # ------------------------------------------------------------------->
    logger.debug(f"[INFO]: start collision analysis")
    for i,mesh in enumerate(mesh_dict.values()):
            is_collision, contact_names = tm_CollManager.in_collision_single(mesh.trimesh,
                                                                    transform=None,
                                                                    return_names=True,
                                                                    return_data=False)
            if is_collision:
                mesh.is_colliding = True
                contact_names.remove(mesh.name)
                mesh.collisions = contact_names
                logger.debug(f"[WARN]: {mesh} is colliding with {contact_names}")
            else:
                logger.debug(f"[INFO]: {mesh} is not colliding")

    # ------------------------------------------------------------------->
    logger.debug(f"[INFO]: calculate and store mesh intersections")
    mesh_x_dict : dict = {}
    for i,mesh in enumerate(mesh_dict.values()):
        if mesh.is_colliding:
            for contact in mesh.collisions:
                mesh_x_name = mesh.name + contact
                if mesh_x_name in mesh_x_dict.keys():
                    continue

                mesh_x = MeshContainer(name=mesh_x_name)
                mesh_x.trimesh = tm.boolean.intersection([mesh.trimesh, mesh_dict[contact].trimesh],
                                                            engine="blender")
                
                if mesh_x.is_watertight:
                    mesh_x_dict[mesh_x.name] = mesh_x
                else:
                    logger.debug(f"[WARN]: Intersection {mesh}-{contact} is not watertight!")

    # ------------------------------------------------------------------->
    logger.debug(f"[INFO]: visualization")
    for mx in mesh_x_dict.values():
        mx.o3dmesh.paint_uniform_color(CLR_ORANGE)

    o3d_txts : list = []
    for mesh in mesh_dict.values():
        o3d_txts.append(util.text_3d(mesh.name,
                                    pos=(mesh.trimesh.centroid),
                                    font_size=30,
                                    density=10))
        if mesh.is_colliding:
             mesh.o3dlineset.paint_uniform_color(CLR_LIGHT_GRAY)
        else:
             mesh.o3dlineset.paint_uniform_color(CLR_BLACK)

    o3d.visualization.draw_geometries([*[mx.o3dmesh for mx in mesh_x_dict.values()],
                                       *[m.o3dlineset for m in mesh_dict.values()],
                                       *o3d_txts])


if __name__ == "__main__":
    main()



