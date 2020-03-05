## Presentation

This docker (*based as the others on geodecision package*):
* can make queries on OSM to get polygons

## Configuration table
> *This table explains the ```config.json``` file*

| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***bbox*** | array | bounding box for the query. ***Must be (SOUTH, WEST, NORTH, EAST) and have an EPSG 4326 (WGS84) projection*** | *[4.81, 45.75, 4.9, 45.81]*|
| ***key*** | str | OSM key tag (*[details here](https://wiki.openstreetmap.org/wiki/Tags#Keys_and_values)*) | *"leisure"*|s
| ***value*** | str | OSM value tag (*[details here](https://wiki.openstreetmap.org/wiki/Tags#Keys_and_values)*) | *"park"* |
| ***driver*** | str | driver to write geospatial file | *"GPKG"*|
| ***output_dir*** | str | output directory | *"outputs"*|

## Inputs/Outputs
* **Input**:""
    * ```config.json```
        *  *example*:
            ```json
            {
            	"bbox": [45.7, 4.82, 45.8, 4.99],
            	"key": "leisure",
            	"value": "park",
            	"driver": "GPKG",
            	"output_dir": "./outputs"
            }
            ```

* **Outputs**:
    * polygons spatial file

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
