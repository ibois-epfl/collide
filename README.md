<h1 align="center">collide</h1>


<p align="center">
    <img src="./img/Screenshot from 2022-11-14 16-43-13.png" width="400">
</p>
<br/>

<div align = "center">
    <a href="https://zenodo.org/badge/latestdoi/561860845"><img src="https://zenodo.org/badge/561860845.svg" alt="DOI"></a>
    <a href = "https://img.shields.io/conda/vn/conda-forge/python">
        <img src = "https://img.shields.io/conda/vn/conda-forge/python" alt = "Conda (channel only)" />
    </a>
    <a href = "https://img.shields.io/badge/python-3.7%20%7C%203.8-brightgreen">
        <img src = "https://img.shields.io/badge/python-3.7%20%7C%203.8-brightgreen" alt = "Conda (channel only)" />
    </a>
    <a href = "https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white">
        <img src = "https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt = "win" height="20"/>
    </a>
    <a href = "https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black">
        <img src = "https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt = "Linux" height="20" />
    </a>
    <a href = "https://github.com/ibois-epfl/augmented-stacking">
        <img src = "https://img.shields.io/badge/license-MIT-green--gray" alt = "License" />
    </a>
</div>
<br/>

<div align = "center">
    <a>
        <img src = "./img/ibosiTraspBlack.png" height="30"/>
    </a>
    <a>
        <img src = "./img/50x50-00000000.png" height="20"/>
    </a>
    <a>
        <img src = "./img/eesd_logo_black.png" height="30"/>
    </a>
    <a>
        <img src = "./img/50x50-00000000.png" height="20"/>
    </a>
    <a>
        <img src = "./img/logoEPFLblack.png" height="30"/>
    </a>
</div>

<br />

**collide** is a simple script to calculate and output data concerning the collision of a set of stones. It is developed in the frame of a collaboration between IBOIS lab (PI: [Andrea Settimi](andrea.settimi@epfl.ch)) and EESD lab (PI: [Savvas Saloustros](savvas.saloustros@epfl.ch)) at EPFL.

In our work we used as metrics to evaluate the success of our scanning techniques: in the case of additive structures, the more intersection you have the less performant your scanning pipeline result to be.

## Usage
You can find some test meshes in the `/data_test` folder. ⚠️ Beware, the meshes need to be *watertight*! ⚠️
### Linux
First install conda and run the following command from the root of the repo:
```bash
conda env create -f environment.yml
conda activate collide
```
For running the script:
```bash
python './collide/src/collide.py' --input_dir="./data/" --output_dir="./out/" --show_3d=0
```
with:
```bash
collide.py
[--input_dir INPUT_DIR] = input directory (path)
[--output_dir OUTPUT_DIR] = output directory (path)
[--show_3d SHOW_3D] = show visualization (0 or 1)
[--print_ply_x PRINT_PLY_X] = save mesh of intersections (0 or 1)
[--print_analysis PRINT_ANALYSIS] = output .txt file with analysis (0 or 1)
[--print_graph PRINT_GRAPH] = output .pdf file with graph (0 or 1)
```
### Windows
 
⚠️ Beware, you need ot install graphviz and include it in PATH before using this script [here!](https://graphviz.org/download/) ⚠️
Run the `collidee.exe` (from the release package) from his folder with the terminal and the following flags:
```powershell
> F:\collide_win\collide.exe --input_dir="./data/" --output_dir="./out/"
```
## Outputs
The script will generate `.txt` file with the following format and data:
```
Standard deviation of object stone pourcentage [%]: 0.45784513381761927
Intersected mesh total volume [m3]: 0.0032008825328167564
index_obj_a index_obj_b mesh_total_obj_pair_vol mesh_intersected_vol pourcentage_split_vol[%]
b f 0.043897394112773866 0.0004255081554947511 0.9693244077350162
c d 0.0385252926335249 0.0012272622917337075 3.185601478509569
...
```
A 3D interactive visualization of the scene.

<div align="center"><img src = "./img/output3d.png" height="300"/></div>

The `.ply` files of the intersected mesh portions, as well as the graph intersection dependency.

<div align="center"><img src = "./img/collision_graph.png" height="300"/></div>

## How to cite
```bibitex
@software{settimicollide2022,
  doi = {10.5281/ZENODO.7324061},
  url = {https://zenodo.org/record/7324061},
  author = {Settimi, Andrea and Gamerro, Julien},
  title = {ibois-epfl/collide: Release v1.0},
  publisher = {Zenodo},
  year = {2022},
  copyright = {Open Access}
}
```
