#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Updated collide

import os
import argparse
import sys

import log
logger = log.setup_custom_logger('root')
from mesh import MeshContainer
import util

import open3d as o3d
import trimesh as tm
import numpy as np
import graphviz
from tqdm import tqdm

mesh_separator = '-' # Separator used between the names of two meshes

def main(input_dir : str,
         output_dir : str,
         show_3d : int,
         print_ply_x : int,
         print_analysis : int,
         print_graph : int,) -> int:

    # ------------------------------------------------------------------->
    logger.debug(f"[INFO]: load meshes on memory files from container")
    mesh_dict : dict = {}
    for i,file in enumerate(os.listdir(input_dir)):
        if file.endswith(".ply"):
            tmp_mesh = MeshContainer(str(file[:-4]))
            tmp_mesh.load_trimesh(input_dir + file)
            mesh_dict[str(file[:-4])] = tmp_mesh

    # ------------------------------------------------------------------->
    logger.debug(f"[INFO]: load meshes to collision manager")
    tm_CollManager : CollisionManager = tm.collision.CollisionManager()
    for mesh in mesh_dict.values():
        tm_CollManager.add_object(mesh.name, mesh.trimesh)

    # ------------------------------------------------------------------->
    logger.debug(f"[INFO]: collision detection and intersection boolean")
    mesh_x_dict : dict = {}
    is_collision, contact_names = tm_CollManager.in_collision_internal(return_names=True,
                                                                       return_data=False)
    print(f"Collision: {contact_names}")
    for coll in tqdm(contact_names, desc="Collision detection", bar_format=util.BFORMAT):
        mesh1_name = coll[0]
        mesh2_name = coll[1]
        mesh1 = mesh_dict[mesh1_name]
        mesh2 = mesh_dict[mesh2_name]
        mesh1.is_colliding = True
        mesh2.is_colliding = True
        mesh1.collisions.add(mesh2_name)
        mesh2.collisions.add(mesh1_name)
        
        mesh_x_name = mesh1_name + mesh_separator + mesh2_name  # Collision name corresponding to two stones  
        mesh_x = MeshContainer(name=mesh_x_name)
        mesh_x.trimesh = tm.boolean.intersection([mesh1.trimesh,mesh2.trimesh], engine="blender")
        
        if mesh_x.trimesh.is_watertight:
            mesh_x_dict[mesh_x_name] = mesh_x
        else:
            mesh_x_dict[mesh_x_name] = mesh_x # Retrieve the name
            logger.debug(f"[ERROR]: Mesh {mesh_x_name} is not watertight. Revise and run again") # Print an error, but do not stop
#            exit(-1)

    # ------------------------------------------------------------------->
    if print_ply_x==0:
        logger.debug(f"[INFO]: output mesh intersections .ply files")

        for file in os.listdir(output_dir):
            if file.endswith(".ply"):
                os.remove(output_dir + file)

        for mesh in tqdm(mesh_x_dict.values(), bar_format=util.BFORMAT):
            mesh.trimesh.export(output_dir + mesh.name + ".ply")
            logger.debug(f"[INFO]: {mesh} exported to {output_dir + mesh.name + '.ply'}")

    # ------------------------------------------------------------------->
    if print_analysis==0:
        logger.debug(f"[INFO]: run analysis/graph on mesh intersections and output to .txt file")
        for file in os.listdir(output_dir):
                if file.endswith(".txt"):
                    os.remove(output_dir + file)
        
        with open(output_dir + "analysis.txt", "w") as f:
            # standard deviation of volume
            std_dev = 0.0
            for mesh in mesh_dict.values():
                if mesh.is_colliding:      
                    mesh_x_volume = 0.0     
                    count = 0
                    for mesh_x in mesh_x_dict.values():
                        if mesh_x.name.startswith(mesh.name): 
                            count +=1 # 
                            mesh_x_volume += mesh_x.volume 
                    mesh.x_volume = mesh_x_volume
                    mesh.x_pourcentage = mesh_x_volume / mesh.volume
#                    std_dev += (mesh.x_pourcentage - 0.5)**2  
#            std_dev = np.sqrt(std_dev / len(mesh_dict))
#            msg_stdev : str = f"Standard deviation of object stone percentage [%]: {std_dev}" 
#            logger.debug(f"[ANSYS]: {msg_stdev}")
#            f.write(msg_stdev + '\n')

            # total volume of the intersections
            total_x_volume = 0.0
            for mesh_x in mesh_x_dict.values():
                total_x_volume += mesh_x.volume
                msg_vol : str = f"Intersected mesh total volume [m3]: {total_x_volume}"
            logger.debug(f"[ANSYS]: {msg_vol}")
            f.write(msg_vol + '\n')

            # output table with values
            msg_header_table = str("index_obj_a" + ' ' +
                                "index_obj_b" + ' ' +
                                "mesh_total_obj_pair_vol" + ' ' +
                                "mesh_intersected_vol" + ' ' +
                                "percentage_split_vol[%]")
            logger.debug(f"[ANSYS]: {msg_header_table}")
            f.write(msg_header_table + '\n')
            for key, value in mesh_x_dict.items():
                sep_index = key.rfind(mesh_separator) # index of mesh separator character
                mesh1_name = key[:sep_index] # mesh name 1
                mesh2_name = key[sep_index+1:] # mesh name 2
                mesh1 = mesh_dict[mesh1_name]
                mesh2 = mesh_dict[mesh2_name]
                
                vol_pair = mesh1.volume + mesh2.volume
                vol_x = value.volume

                pourcentage_split_volume = (vol_x / vol_pair) * 100
                msg_tabel_content = str(mesh1_name + ' ' +
                                        mesh2_name + ' ' +
                                        f"{vol_pair}" + ' ' +
                                        f"{vol_x}" + ' ' +
                                        f"{pourcentage_split_volume}")
                logger.debug(f"[ANSYS]: {msg_tabel_content}")
                f.write(msg_tabel_content + '\n')
    # ------------------------------------------------------------------->
    if print_graph==0:
        logger.debug(f"[INFO]: output collision graph")
        for file in os.listdir(output_dir):
                if file.endswith(".pdf"):
                    os.remove(output_dir + file)

        graph = graphviz.Graph(comment='Collision Graph', strict=True)
        for mesh in mesh_dict.values(): graph.node(mesh.name, color="black")
        for mesh in mesh_dict.values():
            for collision in mesh.collisions:
                graph.edge(mesh.name, collision)
        graph.render(output_dir + "collision_graph", view=False)

    # ------------------------------------------------------------------->
    if show_3d==0:
        logger.debug(f"[INFO]: visualization")
        for mx in mesh_x_dict.values():
            mx.o3dmesh.paint_uniform_color(util.Clr.ORANGE.value)

        o3d_txts : list = []
        for mesh in mesh_dict.values():
            o3d_txts.append(util.text_3d(mesh.name,
                                        pos=(mesh.trimesh.centroid),
                                        font_size=30,
                                        density=10))
            if mesh.is_colliding:
                mesh.o3dlineset.paint_uniform_color(util.Clr.LIGHT_GRAY.value)
            else:
                mesh.o3dlineset.paint_uniform_color(util.Clr.BLACK.value)

        o3d.visualization.draw_geometries([*[mx.o3dmesh for mx in mesh_x_dict.values()],
                                        *[m.o3dlineset for m in mesh_dict.values()],
                                        *o3d_txts])
    
    return 0


if __name__ == "__main__":
    # create command line parser
    parser = argparse.ArgumentParser(description='Mesh Intersection Analysis')
    parser.add_argument('--input_dir', type=str,
                        help='input directory')
    parser.add_argument('--output_dir', type=str,
                        help='output directory')
    parser.add_argument('--show_3d', type=int, default=0,
                        help='show visualization')
    parser.add_argument('--print_ply_x', type=int, default=0,
                        help='save mesh of intersections')
    parser.add_argument('--print_analysis', type=int, default=0,
                        help='output .txt file with analysis')
    parser.add_argument('--print_graph', type=int, default=0,
                        help='output .pdf file with graph')

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    _input_dir : str
    _output_dir : str
    _show_3d : int
    _print_ply_x : int
    _print_analysis : int
    _print_graph : int
    
    if args.input_dir is not None: _input_dir = args.input_dir
    else:
        raise ValueError("input_dir is not defined")
    if args.output_dir is not None:
        _output_dir = args.output_dir
    else:
        _output_dir = "./output/"
    if not os.path.exists(_output_dir):
        os.makedirs(_output_dir)

    if args.show_3d is not None: _show_3d = args.show_3d
    if args.print_ply_x is not None: _print_ply_x = args.print_ply_x
    if args.print_analysis is not None: _print_analysis = args.print_analysis
    if args.print_graph is not None: _print_graph = args.print_graph

    logger.debug(f"[CMDLN]: input_dir: {_input_dir}")
    logger.debug(f"[CMDLN]: output_dir: {_output_dir}")
    logger.debug(f"[CMDLN]: show_3d: {_show_3d}")
    logger.debug(f"[CMDLN]: print_ply_x: {_print_ply_x}")
    logger.debug(f"[CMDLN]: print_analysis: {_print_analysis}")
    logger.debug(f"[CMDLN]: print_graph: {_print_graph}")

    main(input_dir = _input_dir,
         output_dir = _output_dir,
         show_3d = _show_3d,
         print_ply_x = _print_ply_x,
         print_analysis = _print_analysis,
         print_graph = _print_graph)
