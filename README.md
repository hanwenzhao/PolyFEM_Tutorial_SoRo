# Generate Vision Proprioception Data for Defomable Objects using PolyFEM

TODO: insert simulation animation

PolyFEM is a simple and user-friendly finite element library that handles complex contact configurations under a variety of external conditions, resulting in a robust and accurate simulation of elastic objects. In this tutorial, we will demostrate how PolyFEM can be used to generate vision proprioception data for soft robotics study.

[ToC]

###### tags: `Soft Robotics`, `Deformable Objects`, `Kinetmatics`, `Data Generation`

## Prerequisite
Following items are necessary to complete this tutorial. To replicate the experiment, readers can use either the given mesh files or their own mesh files.

In this tutorial, we assume that readers already have PolyFEM install in their machine. If not, the PolyFEM install instruction can be found [here](https://polyfem.github.io/#polyfem-in-c). After compilation of C++ code, an executable can be found `.../polyfem/build/PolyFEM_bin`.


- [ ] PolyFEM Installation

To decrease the computing complexity of this tutorial example, we assume that the target item is the only deformable solid and the environment is rigid and immovable.

- [ ] Target Object Mesh
TODO: insert screenshot
- [ ] Environment Mesh
TODO: insert screenshot

## Problem Formulation
This tutorial's objective is to launch a deformable target object into an environment mesh (i.e. a sphere rolling in a bowl) and gather the corresponding vision-based proprioceptive data (internal view that shows deformation). Such data can be utilized to investigate the relationship between vision-based proprioception and kinematics.

## Simulation Setup
PolyFEM provides interface through JSON and Python. Here we demonstrate the JSON interface setup first.
### JSON Script
We split the setting into two different JSON files, where the `default.json` contains simulation level configurations and `scene_bowl.json` contains scene level configuration. For more details, please refer to the [JSON API](https://polyfem.github.io/json/).
#### Simulation Level Json
The `default.json` defines high level simulation setting. For example, we define our problem as `Generic Tensor` and we use `NeoHookean` as our tensor formulation. Next, we can set `is_time_dependent` to `true` in `problem parameters` to enable sequential output. 
Also, it is necessary to define the non-linear solver you would like to use and setting corresponding parameters. `has_collision` enables collision check and allow interactions between the target object and environment object.

default.json
```json=
{
    "problem": "GenericTensor",
    "tensor_formulation": "NeoHookean",

    "problem_params": {
        "is_time_dependent": true
    },

    "nl_solver": "newton",
    "solver_params": {
        "mtype": 2,
        "gradNorm": 1e-5,
        "useGradNorm": false
    },
    "solver_type": "Eigen::PardisoLDLT",
    "line_search": "backtracking",
    "project_to_psd": true,
    "lump_mass_matrix": true,

    "has_collision": true,

    "normalize_mesh": false,

    "export": {
        "paraview": "sol.vtu",
        "body_ids": true,
        "material_params": true
    },
    "quadrature_order": 1,
    "save_time_sequence": true,
    "save_solve_sequence_debug": false,
    "vismesh_rel_area": 10000000,
    "output": "sim.json"
}
```


#### Scene Level JSON
In the scene level json script, we first load simualtion level json configuration by setting the `default_params` to the path of the `default.json`. Then, we can define gravity as `"rhs": [0, 9.81, 0]`, and give the target object a initial velocity by setting `initial_velocity` with mesh body id. Moreover, the simuation time can be set using `tend`, and time step size throgh `dt`.

In the `meshes`, we provide the path to the target object mesh, and define its material properity with Young's modulus `E`, Poisson's ratio `nu`, and density `rho`.

We use [obstacles](https://polyfem.github.io/json/#obstacles) to define the environment object since it is a formal way of specifying non-simulated collision object in PolyFEM. Obstacles are considered rigid in PolyFEM and only the surface are taken into consideration, accelerate the simualtion process.

scene_bowl.json

```json=
{
    "default_params": "default.json",
    "problem_params": {
        "rhs": [0, 9.81, 0],
        "initial_velocity": [{
            "id": 1,
            "value": [5, 0, 0]
        }]
    },

    "tend": 10.0,
    "dt": 0.1,
    "dhat": 1e-4,
    "epsv": 4e-3,
    "mu": 0.5,
    "friction_iterations": 1, 

    "meshes": [{
        "mesh": "data/sphere1K.msh",
        "position": [0, 2, 0],
        "body_id": 1,
        "scale": 1.0
    }],

    "body_params": [{
        "id": 1,
        "E": 5e3,
        "nu": 0.3,
        "rho": 100
    }],

    "obstacles": [{
        "mesh": "data/Scene_Disk.msh",
        "position": [0, 0, 0],
        "scale": 0.1,
        "enabled": true
    }],

    "output": "results.json",
    "save_solve_sequence_debug": false,
    "export": {
        "time_sequence": "output.pvd",
        "paraview": "result.vtu",
        "body_ids": true,
        "material_params": true
    },
    "save_time_sequence": true
}
```
