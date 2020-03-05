## Presentation
Get buildings from GML file & make some measures on roofs and grounds :
* slope,
* area,
* total surface,
* compactness (*see:https://fisherzachary.github.io/public/r-output.html*)
* minimum_width based on minimum_rotated_rectangle (*see: https://shapely.readthedocs.io/en/stable/manual.html#object.minimum_rotated_rectangle*)

## Configuration table
> *This table explains the ```config.json``` file*.

### Sections
| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***epsg*** | int | ***see [epsg section](#epsg)*** | |
| ***dir*** | str | ***see [dir section](#dir)*** | |
| ***settings*** | str | ***see [settings section](#settings)*** | |

#### epsg
| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***in*** | int | Value for input EPSG | *3946*|
| ***out*** | int | Value for output EPSG | *3946*|

##### dir
| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***input*** | str | directory of input GML files | *"data/CityGML/"*|
| ***output*** | str | directory for results/outputs files | *"data/outputs/"*|

#### settings
| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***palette*** | str | ***name of color palette*** | "viridis" |
| ***driver*** | str | driver for output (*"GPKG","GeoJSON"*) | *"GPKG"*|
| ***attributes*** | array | attributes to search/qualify public access buildings | *["ADMINISTRA", "CULTE", "DEPLACEMEN"]*|

#### Complete example JSON
```JSON
{
	"epsg": {
		"in":3946,
		"out":3946
	},
	"dir":{
		"input":"data/CityGML/",
		"output":"data/outputs/"
	},
	"settings":{
		"palette":"viridis",
		"driver":"GPKG",
		"attributes":[
			"ADMINISTRA",
		    "CULTE",
		    "DEPLACEMEN",
		    "ENSEIGNEME",
		    "SANTE",
		    "SPORT",
		    "URGENCE"
		]
	}
}
```

## Inputs/outputs
* **Inputs**:
	* ```config.json```
* **Outputs**:
	* roofs geospatial file (*buildings roofs with measures*)
	* grounds geospatial file (*grounds of buildings*)
	* JSON buildings file (*with buildings attributes*)

## Build
> *following command works inside the FormatAndAnalyseRoofs/DockerContext/ directory*

```bash
sudo docker build --build-arg git_token=<TOKEN> -t roofs <DockerContext>
```

## Run
> *following command works inside the FormatAndAnalyseRoofs/ directory*

```bash
sudo docker run --mount src=`pwd`,target=/Input,type=bind --mount src=`pwd`,target=/Output,type=bind -it roofs
```
