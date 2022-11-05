#!/usr/bin/env python

import open3d as o3d
import trimesh as tm
from mesh import MeshContainer
import numpy as np


def main() -> None:

    # 1 load objects on memory
    # 2 for each stone which understand which of the other stones and create a graph

    # mesh_A = pymesh.load_mesh("A.ply")
    # mesh_B = pymesh.load_mesh("B.ply")

    DATA_DIR : str = "./data/"
    OUT_DIR : str = "./out/"
    # mesh_A = o3d.io.read_triangle_mesh(DATA_DIR + "m_A.ply")
    # mesh_B = o3d.io.read_triangle_mesh(DATA_DIR + "m_B.ply")
    # mesh_C = o3d.io.read_triangle_mesh(DATA_DIR + "m_C.ply")

    # convert to pymesh as trimesh object
    mesh_A = MeshContainer("A")
    mesh_A.load_trimesh(DATA_DIR + "m_A.ply")
    mesh_B = MeshContainer("B")
    mesh_B.load_trimesh(DATA_DIR + "m_B.ply")
    mesh_C = MeshContainer("C")
    mesh_C.load_trimesh(DATA_DIR + "m_C.ply")

    # # set all the meshes in an array
    mesh_containers : list = [mesh_A, mesh_B, mesh_C]

    # calculate the collisions of each mesh
    tm_CollManager = tm.collision.CollisionManager()
    tm_CollManager.add_object("A", mesh_A.trimesh)
    tm_CollManager.add_object("B", mesh_B.trimesh)
    tm_CollManager.add_object("C", mesh_C.trimesh)

    is_contact, contact_names = tm_CollManager.in_collision_single(mesh_A.trimesh,
                                                                    transform=None,
                                                                    return_names=True,
                                                                    return_data=False)

    mesh_A.is_colliding = is_contact
    mesh_A.collisions = contact_names

    res = tm.boolean.intersection([mesh_A.trimesh, mesh_B.trimesh], engine="blender")
    print(f"Volume of intersection: {res.volume}")



    # visualizer


    # o3d_res = res.as_open3d.paint_uniform_color([1, 0.706, 0])
    o3d_res = res.as_open3d.paint_uniform_color([1, 0.706, 0])
    # o3d_res = o3d.geometry.LineSet.create_from_triangle_mesh(o3d_res).paint_uniform_color([1, 0.706, 0])
    meshB = mesh_B.trimesh.as_open3d
    meshB = o3d.geometry.LineSet.create_from_triangle_mesh(meshB)
    meshA = mesh_A.trimesh.as_open3d
    meshA = o3d.geometry.LineSet.create_from_triangle_mesh(meshA)


    # # option1
    # mat = o3d.visualization.rendering.MaterialRecord()
    # mat.base_color = np.array([1, 1, 1, .5])
    # o3d.visualization.draw({'name': 'test', 'geometry': o3d_res, 'material': mat})

    # # option 2
    # o3d_visualizer = o3d.visualization.Visualizer()
    # o3d.visualization.rendering.MaterialRecord.base_color = [1, 0.706, 0, 0.5]
    # # rndr = o3d_visualizer.get_render_option().mesh_color_option
    # o3d_visualizer.create_window()
    # o3d_visualizer.add_geometry(o3d_res)
    # o3d_visualizer.add_geometry(mesh_A.trimesh.as_open3d.paint_uniform_color([1, 0, 0]))
    # o3d_visualizer.run()
    # o3d_visualizer.destroy_window()

    # option 3
    o3d.visualization.draw_geometries([o3d_res, meshB, meshA])



if __name__ == "__main__":
    main()



