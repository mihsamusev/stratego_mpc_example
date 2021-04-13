# Stratego MPC example
Minimal example running UPPAAL Stratego as a part of model predictive control MPC loop using [`strategoutil`](https://github.com/mihsamusev/strategoutil.git).

## Installation

This example uses helper library [strategoutil](https://github.com/mihsamusev/strategoutil.git)
```
git clone https://github.com/mihsamusev/strategoutil.git
cd strategoutil
pip install -e .
```

## Example
Describes a toy example traffic control of one way road intersections based on _Eriksen et al., 2020, Controlling Signalized Intersections using Machine Learning_ ([link to paper](https://doi.org/10.1016/j.trpro.2020.08.127)).

<p align="center">
  <img width="400" src="docs/plant.png">
</p>

Corresponding UPPAAL stratego model is found in `uppaal/model.xml`. The task of the MPC control loop iteratively to re-build the model with updated/measured queue lengths `S` and `E`, and calculate optimal control strategy up to horizon. This re-building happends by using `uppaal/model_template.xml` where important variables are commented out with a specific patterns/tags known to the user. [`strategoutil`](https://github.com/mihsamusev/strategoutil.git) then allows to replace those tags with values. For simplicity of the example, measureable disturbances such as vehicle inflow/outflow rates `r` are not inserted back into the model and stay costant.

To run the example use `example.py` script, the only thing you need to customize is the path to UPPAAL Stratego `verifyta` stored in `verifyta_path` variable. 

## Control loop

<p align="center">
  <img width="800" src="docs/loop.png">
</p>

To accomodate shown MPC loop, the project consists of couple of files:

- `*.xml` template file describing UPPAAL model where changing variables commented out with known tags. Folder `uppaal/` contains original `model.xml`, and `model_template.xml` where variables are substitued by tags.
- `model_interface.py` that leverages `StrategoController` class and functions of `strategoutil` to create the interface to exclusively interact with `model_template.xml`.
- `example.py` that puts it all together and showcases the MPC control loop
- [optional] `*.yaml` configuration file with `verifyta` arguments, in the example default arguments are used
- [optional] `*.q` file specifying Stratego query, in the example query inside `model_template.xml` will be used


## Some inserting tricks
Maybe its not a good idea to crete tags that contain `<>` characters, since in `*.xml` file they are written as `&lt;` or `&lt;`, which might lead to confusion. A simplest alternative is just to add `\\TAG_` in front of your variable name.