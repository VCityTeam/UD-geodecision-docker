## Presentation

This docker (*based as the others on geodecision package*):
* get OpenStreetMap network,
* transforms it into graph
* add edges values

## Configuration table
> *This table explains the ```config.json``` file*

| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***bbox*** | array | bounding box to get graph, can be set with [Geofabrik Tile Calculator](http://tools.geofabrik.de/calc/) [left, bottom, right, top]   | *[4.81, 45.75, 4.9, 45.81]*|
| ***network_type*** | str | type of the network | *"walk"*|
| ***simplify*** | boolean | simplify or not the graph | *false*|
| ***walk_distance*** | integer | distance in meters walkable within 1 hour | *5000*|
| ***output_dir*** | str | output directory | *outputs*|
| ***nodes_name*** | str | name of the nodes JSON file | *nodes.json*|
| ***nodes_name*** | str | name of the edges JSON file | *edges.json*|

## Inputs/Outputs
* **Input**:
    * ```config.json```
* **Outputs**:
    * nodes JSON file
    * edges JSON file

## Build
> *following command works inside the Dashboard/DockerContext directory*

```bash
sudo docker build --build-arg git_token=<TOKEN> -t get_graph <DockerContext>
```

## Run
> *following command works inside the Dashboard/ directory*

```bash
sudo docker run --mount src=`pwd`,target=/Input,type=bind --mount src=`pwd`,target=/Output,type=bind -it get_graph
```
