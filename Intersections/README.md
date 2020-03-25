## Presentation
This docker classifies potential intersected (*multi-*)polygons (*GPKG*) according to intersecting (*multi-*)polygons (*GPKG*):
* spatial intersections between potential intersected and intersecting, for example, rooftops and walkable isochrones,
* rooftops intersected will get the value of intersecting

***Input files must be GPKG and intersecting layers name must contain integers that will be used as classe's names for ```classes``` new field in output file.***:
* intersecting GPKG layers example:
	* "*isochrone_5_mns*"
	* "*isochrone_10_mns*"
	* "*isochrone_15_mns*"

## Configuration table
> *This table explains the ```config.json``` file*.

| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***output*** | str | path to output/result file | "*outputs/results.gpkg*" |
| ***source_gpkg*** | str | path to source GPKG file (*polygons to intersect*) | "*data/Roofs.gpkg*" |
| ***intersecting_gpkg*** | str | path to intersecting GPKG file | "*data/iso_cut.gpkg*" |
| ***epsg*** | int | EPSG for intersections and output | *2154* |
| ***quadrat_width*** | int | width (*in EPSG units*) for Rtree grid cutting | *200* |
| ***driver*** | str | driver for output | "*GPKG*" |


#### Complete example JSON
```JSON
{
	"output" : "outputs/results.gpkg",
	"source_gpkg": "data/Roofs.gpkg",
	"intersecting_gpkg": "data/iso_cut.gpkg",
	"epsg":2154,
	"quadrat_width": 200,
	"driver": "GPKG"
}
```

## Inputs
* ```config.json```

## Build
Build (*following command works inside the Dashboard/DockerContext directory*)

```bash
sudo docker build --build-arg git_token=<TOKEN> -t intersections DockerContext
```

## Run
> *following command works inside the Intersections/ directory*

```bash
sudo docker run --mount src=`pwd`,target=/Input,type=bind --mount src=`pwd`,target=/Output,type=bind -it intersections
```
