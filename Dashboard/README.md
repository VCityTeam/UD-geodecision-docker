## Presentation
This docker allow to run a webmapping decision-making tools application locally through your favorite web browser.

## Configuration table
> *This table explains the ```config.json``` file*. It contains list of settings (*because the ClassificationDataFrames from geodecision can loop on multiple variables and files*). The table shows a typical element of a list.

### Sections
| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***inputs*** |  | ***see [inputs section](#inputs)*** | |
| ***figures_settings*** |  | ***see [figures_settings section](#figures_settings)*** | |

#### inputs
| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***roofs*** | str | name of the inpu geospatial roofs file | *"dashboard/data/Dashboard/Roofs.gpkg"*|
| ***background*** | str | GeoJSON input file for background, default, included in the Docker | *"dashboard/background.geojson"*|
| ***accessibility*** |  | ***see [accessibility section](#accessibility)*** | *|
| ***layers*** | array | List of layers that will be used in the Bokeh app | *["LYON1ERBATI2015", "LYON9EMEBATI2015", "VILLEURBANNEBATI2015"]*|

##### accessibility
| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***origins*** | str | origin polygons input geospatial file | *"dashboard/data/Dashboard/parks.geojson"*|
| ***isochrones*** | str | isochrones/isolines input geospatial file | *"dashboard/data/Dashboard/iso_cut.gpkg"*|
| ***layers*** | array | List of layers that will be used in the Bokeh app | *["iso_1", "iso_2", "iso_3"]*|

#### figures_settings
| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***figure_range*** |  | ***see [figure_range section](#figure_range)*** | |
| ***values*** | array | fields in ```roofs``` that will be used as filters (*Bokeh range sliders*)  | *["angles", "heights","area", "total_surface", "min_width", "compactness"]*|
| ***samples*** | int | value to split filter/field in *n* elements | *100*|
| ***group*** | str | column field used to group data | *"NOMCOMMUNE"*|
| ***table_columns*** | array | list of field column names that will be kept from the origin roofs source file | *["attribute", "public_access", "angles", "heights", "nb_levels", "area", "total_surface",]*|
| ***iso_alpha*** | float | Default value for isochrones fill-alpha | *0.1*|

##### figure-range
###### x_range
| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***left*** | real | left/west value for the figure range (***requires ESPG:3857 value***) | *535140*|
| ***left*** | real | right/east value for the figure range (***requires ESPG:3857 value***) | *547883*|

###### y_range
| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***bottom*** | real | bottom/south value for the figure range (***requires ESPG:3857 value***) | *5735333*|
| ***top*** | real | top/north value for the figure range (***requires ESPG:3857 value***) | *5746576*|

#### Complete example JSON
```JSON
{
	"inputs": {
		"roofs": "dashboard/data/Dashboard/Roofs.gpkg",
		"background": "dashboard/background.geojson",
		"accessibility": {
			"origins": "dashboard/data/Dashboard/parks.geojson",
			"isochrones": "dashboard/data/Dashboard/iso_cut.gpkg",
			"layers": [
				"iso_1",
				"iso_2",
				"iso_3",
				"iso_4",
				"iso_5",
				"iso_6",
				"iso_7",
				"iso_8",
				"iso_9",
				"iso_10"
			]
		},
		"layers": [
			"LYON1ERBATI2015",
			"LYON2EMEBATI2015",
			"LYON3EMEBATI2015",
			"LYON4EMEBATI2015",
			"LYON5EMEBATI2015",
			"LYON6EMEBATI2015",
			"LYON7BATI2015",
			"LYON8EMEBATI2015",
			"LYON9EMEBATI2015",
			"VILLEURBANNEBATI2015"
		]
	},
	"figures_settings": {
		"figure_range": {
			"x_range": {
				"left": 535140,
				"right": 547883
			},
			"y_range": {
				"bottom": 5735333,
				"top": 5746576
			}
		},
		"values": [
			"angles",
			"heights",
			"area",
			"total_surface",
			"min_width",
			"compactness"
		],
		"samples": 100,
		"group": "NOMCOMMUNE",
		"table_columns": [
			"building_ids",
			"ADRESSE",
			"attribute",
			"public_access",
			"angles",
			"heights",
			"nb_levels",
			"area",
			"total_surface",
			"min_width",
			"compactness"
		],
		"iso_alpha":0.1
	}
}
```

## Inputs
* ```bokeh_config.json```

## Build
Build (*following command works inside the Dashboard/DockerContext directory*):
    ```bash
    sudo docker build --build-arg git_token=<TOKEN> -t dashboard_app DockerContext
    ```
## Run
Run => In order to get the Bokeh Dashboard app running in docker but stay accessible from the web browser host, ports need to be set with the ```-p``` argument (*following command works inside the Dashboard/ directory*) :
```bash
sudo docker run --mount src=`pwd`,target=/Input,type=bind,type=bind -p 5006:5006 -it dashboard_app
```
* Then, go to => http://localhost:5006/dashboard
* You should get something like this:
![presentation](../img/dashboard_presentation.png)

## Interface explanations
* **Filter/Selection widgets section** (*filter and selection applied only after clicking on the **Filter button***)
    * A selection roofs layer widget
    * Radio button to select all buildings or only "*public access buildings" (schools, museum, hospital, ...)*
    * Range sliders to filter with minimum and maximum value for each filter
    * Filter button => apply selection and filter
    * Reset button => reset all filters and selections but don't reset data
* It is divided into **3 Panels**:
    * **Map**:
        * ***Figure*** => Dynamic and interactive Bokeh map figure element
        * ***Widgets***:
            * Classical Bokeh widgets on the right of the map (*pan, zoom, reset, ...*)
            * Legend widget to hide/show element by clicking on it
            * 2 color pickers:
                * one to change the isochrone layer color,
                * the other one to change the building color layer
            * 3 sliders:
                * Simple slider to change background opacity  
                * Simple slider to show/hide isochrones layer
                * Range slider to show isochrone layers
    * **Datatable**:
        * Bokeh Datatable showing selected/filtered data (*same as data shown on map*)
    * **Synthesis**:
        * Histogram showing filtered data sum by districts/towns
        * Synthesis for selected layer and filtered data  
