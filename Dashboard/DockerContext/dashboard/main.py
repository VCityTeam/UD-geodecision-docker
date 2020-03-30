#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 11:53:54 2020

@author: thomas
"""
from bokeh.models import ColumnDataSource, GeoJSONDataSource, HoverTool, Panel, Tabs
from bokeh.palettes import Viridis11
from bokeh.transform import factor_cmap
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models.widgets import Button, Select, DataTable, TableColumn, RadioGroup, Div, ColorPicker, Slider, RangeSlider
from bokeh.layouts import row, widgetbox, column, Spacer
from bokeh.io import curdoc
import json
import sys
import geopandas as gpd
from shapely.geometry import LineString

#TODO change to from geodecision after tests
from bokeh_snippets import make_sliders, get_hist_source
from geodecision import gdf_to_geosource
from constants import set_para


#####################
# GET PARAMS & DATA #
#####################
#Get json_config from arg
json_config = sys.argv[1]

#Load params JSON file
with open(json_config) as f: 
    params = json.load(f)
values = params["figures_settings"]["values"]
samples = params["figures_settings"]["samples"]
group = params["figures_settings"]["group"]

#Get one gdf
columns = params["inputs"]["columns"]
columns.append("geometry")
gdfs = []
for layer in params["inputs"]["layers"]:
    gdfs.append(
            gpd.GeoDataFrame.from_file(
                    params["inputs"]["roofs"],
                    layer=layer
                    )[columns]
            )
gdf = gpd.pd.concat(gdfs)

#Simplify with topology preservation in order to improve performance
gdf["geometry"] = gdf["geometry"].simplify(0.1)
#Transform polygons to LineStrings in order to improve performance with webgl
##see https://docs.bokeh.org/en/latest/docs/user_guide/webgl.html#support
gdf["geometry"] = gdf["geometry"].map(lambda x: LineString(x.exterior.coords))


#Add alpha & color columns for futur use
gdf["alpha"] = 1.0
gdf["color"] = "white"

#Set angles max base value (limit number of polygons on screen)
angles_value_max_base = 30.0

#Source for map
## Reprojection to fit with Bokeh tiles
gdf = gdf.to_crs(epsg=3857)
## Get intersections and update gdf
ids = params["inputs"]["unique_id"]
classes = params["inputs"]["classes"]
intersections = gpd.GeoDataFrame.from_file(
    params["inputs"]["intersections"]
    )[[ids, classes]]
gdf = gdf.merge(intersections[[ids, classes]], on=ids)

#Split dict column into multiple columns
gdf[classes] = gdf[classes].map(json.loads)
df = gpd.pd.DataFrame.from_records(gdf[classes].tolist())
cols =[]
for col in list(df.columns):
    gdf[col] = df[col]
    cols.append(col)

#Manage layers
layers = list(gdf[group].unique())
default = layers[0]

## Transform to GeoJSONDataSource
geo_source = GeoJSONDataSource(
        geojson=gdf_to_geosource(
                gdf.loc[
                    (gdf[group] == default)
                    & (gdf["angles"] <= angles_value_max_base)
                    ]
                )
        )
## Source for Datatable
table_source = ColumnDataSource(
        gdf[
                params["figures_settings"]["table_columns"]
                ].loc[gdf[group] == default]
        )

## Source for accessibility
access = {}
access_slider_control = {} 
for i,layer in enumerate(params["inputs"]["accessibility"]["layers"]):
    #Try to improve performance with simplification
    ##see https://shapely.readthedocs.io/en/latest/manual.html#object.simplify
    tmp = gpd.GeoDataFrame.from_file(
        params["inputs"]["accessibility"]["isochrones"],
        layer=layer
        ).to_crs(epsg=3857)
    tmp["geometry"] = tmp["geometry"].simplify(0.1)
    access[layer] = GeoJSONDataSource(
                geojson=gdf_to_geosource(
                        tmp
                        )
                    )
    access_slider_control[i] = layer

### Get origins
origins_source = GeoJSONDataSource(
            geojson=gdf_to_geosource(
                    gpd.GeoDataFrame.from_file(
                            params["inputs"]["accessibility"]["origins"]
                            ).to_crs(epsg=3857)
                    )
                )

## Background layer
background_source = GeoJSONDataSource(
        geojson=gdf_to_geosource(
                gpd.GeoDataFrame.from_file(params["inputs"]["background"])
                )
        )

## Figure range
x_range = (
        params["figures_settings"]["figure_range"]["x_range"]["left"],
        params["figures_settings"]["figure_range"]["x_range"]["right"]
        )
y_range = (
        params["figures_settings"]["figure_range"]["y_range"]["bottom"],
        params["figures_settings"]["figure_range"]["y_range"]["top"]
        )

#############
# FUNCTIONS #
#############    
def update(new):
    button.disabled = True
    tmp = None
    #Loc on selection range sliders min and max
    for k,v in sliders.items():
        if v.value is not None:
            start = v.value[0]
            end = v.value[1]
            if tmp is None:
                tmp = gdf.loc[
                        (gdf[k] >= start) 
                        & (gdf[k] < end)
                        ]
            else:
                tmp = tmp.loc[
                        (tmp[k] >= start) 
                        & (tmp[k] < end)
                        ]
    #Loc on isochrone range sliders min and max
    min_iso = str(int(round(iso_progression_slider.value[0])))
    max_iso = str(int(round(iso_progression_slider.value[1])))
    if tmp is not None:
        if min_iso == "0": 
            inside = tmp.loc[tmp[max_iso] == True]
            outside = tmp.loc[tmp[max_iso] == False]
        else:
            inside = tmp.loc[
                (tmp[min_iso] == True) 
                & (tmp[max_iso] == True)
                ]
            outside = tmp.loc[
                (tmp[min_iso] == False) 
                & (tmp[max_iso] == False)
                ]
        
        for index in outside.index:
            tmp.at[index, "color"] = "red"
        
    if radio_group.active == 1:
        tmp = tmp.loc[tmp["public_access"] == True]
    tmp_map = tmp.loc[tmp[group] == select.value]
    
    #Get elements for map and synthesis
    hist_source.data = get_hist_source(tmp, group)
    geo_source.geojson = gdf_to_geosource(tmp_map)
    table_source.data = inside[params["figures_settings"]["table_columns"]]
    button.disabled = False

    para.text = set_para(
            gdf[
                    params["figures_settings"]["table_columns"]
                    ].loc[gdf[group] == select.value],
            tmp_map,
            sliders,
            select.value,
            min_iso,
            max_iso
            )

def reset(new):
    for slider in sliders.values():
        slider.value = (slider.start, slider.end)
    radio_group.active = 0
    
def get_iso_layer(attr, old, new):
    start = int(round(iso_progression_slider.value[0]))
    end = int(round(iso_progression_slider.value[1]))
    for k,v in access_slider_control.items():
        selected = map_.select_one({"name":access_slider_control[k]})
        if k in range(start, end+1):
            selected.visible =True
        else:
            selected.visible = False
            
#######################
# WIDGETS AND FIGURES #
#######################
#Tiles
tile_provider = get_provider(Vendors.STAMEN_TERRAIN)
#Create sliders
##Filter sliders
sliders = make_sliders(gdf, values, samples=samples)
##Iso progression slider
keys = list(access_slider_control.keys())
iso_progression_slider = RangeSlider(
        start=0, 
        end=keys[-1], 
        step=keys[1]-keys[0], 
        title="Isochrones progression",
        value=(0,1)
        )
iso_progression_slider.on_change("value",get_iso_layer)
#Create buttons
button = Button(label="Filter", button_type="success")
reset_button = Button(label="Reset", button_type="warning")

#Create color picker for isochrones
color_picker_iso = ColorPicker(
        color="#ff4466", 
        title="Choose isochrones color:", 
        width=200
        )

#Create select box
select = Select(
        title="Layer:", 
        value=default, 
        options=layers
        )

#HISTOGRAM
#Source for histogram
hist_source = ColumnDataSource(data=get_hist_source(gdf, group)) 
hist = figure(
    x_range=hist_source.data["groups"], 
    plot_height=400, 
    plot_width=600,
    toolbar_location=None, 
    title="Number of rooftops's polygons per area"
)

hist.vbar(
       x="groups", 
       top="sums", 
       width=0.9, 
       source=hist_source, 
       legend_field="labels",
       line_color='white', 
       fill_color=factor_cmap(
           "groups", 
           palette=Viridis11, 
           factors=hist_source.data["groups"]
       )
      )

hist.xgrid.grid_line_color = None
hist.legend.orientation = "vertical"
hist.legend.label_text_font_size = "8pt"
hist.xaxis.major_label_orientation = 1
new_legend = hist.legend[0]
hist.legend[0] = None
hist.add_layout(new_legend, 'right')

#MAP
map_ = figure(
        title="Map",
        output_backend="webgl",
        plot_height=800,
        plot_width=800,
        x_range = x_range,
        y_range = y_range
        )

#Add tile
map_.add_tile(tile_provider)

#Add background
background = map_.patches(
        "xs",
        "ys",
        fill_color = "black",
        fill_alpha = 0.5,
        line_alpha = 0.0,
        source=background_source,
        name="background"
        )
## Create linked opacity layer slider
back_slider = Slider(
        start=0, 
        end=1, 
        value=0.5, 
        step=.1, 
        title="Background Opacity"
        )
back_slider.js_link("value", background.glyph, "fill_alpha")

#Add isochrones patches
color_access = "green"
fill_alpha = params["figures_settings"]["iso_alpha"]
access_glyphs = []
for i, (layer, source) in enumerate(access.items()):
    if i <= 1:
        visible=True
    else:
        visible=False
    access_glyphs.append(
            map_.patches(
                "xs", 
                "ys", 
                fill_color=color_access,
                line_color="white",
                fill_alpha = fill_alpha,
                line_alpha=0.0,
                line_width=0.0,
                source=source,
                name=layer,
                visible=visible,
                legend_label=layer
                )
            )
## Create linked opacity isochrones slider
iso_alpha_slider = Slider(
        start=0, 
        end=fill_alpha, 
        value=fill_alpha, 
        step=fill_alpha, 
        title="Iso Opacity ON/OFF",
        width = 30
        )
   
#Link color picker and alpha slider to isochrones color glyph
for glyphs in access_glyphs:
    color_picker_iso.js_link("color", glyphs.glyph, "fill_color")
    iso_alpha_slider.js_link("value", glyphs.glyph, "fill_alpha")

#Add building patches
buildings = map_.multi_line(
        "xs", 
        "ys", 
        line_color="color",
        alpha="alpha",
        width=0.2,
        source=geo_source,
        name="buildings",
        legend_label="Roofs"
        )

#Add origins patches
origins = map_.patches(
        "xs", 
        "ys", 
        fill_color="blue",
        line_color="white",
        fill_alpha = 0.0,
        line_alpha=0.5,
        line_width=0.5,
        source=origins_source,
        name="origins",
        legend_label="Origins"
        )

##Add legend (MUST BE AFTER ADDING LAYERS TO LEGEND)
map_.legend.location = "top_right"
map_.legend.click_policy="hide"
map_.legend.background_fill_alpha = 0.7
map_.legend.background_fill_color = "black"
map_.legend.label_text_color = "white"

#DATATABLE & Tooltips
columns = []
tooltips = []
for col in params["figures_settings"]["table_columns"]:
    columns.append(
            TableColumn(
                    field=col, 
                    title=col
                    )
            )
    tooltips.append(
            (col, "@" + col)
            )

data_table = DataTable(
        source=table_source, 
        columns=columns,
        height=600,
        width=800
        )

#RADIOGROUP
radio_group = RadioGroup(
        labels=["All buildings", "Only public access buildings"], active=0)

#DIV
sub_title = Div(
    text="""
    Rooftops's polygons filtering. 
    A
    """, 
    width=200, 
    height=100
    )

#PARAGRAPH
para = Div(
        text="""""",
        width=600, 
        height=400
        )
min_iso = str(int(round(iso_progression_slider.value[0])))
max_iso = str(int(round(iso_progression_slider.value[1])))
col_for_para = params["figures_settings"]["table_columns"]
col_for_para.extend(cols)

para.text = set_para(
            gdf[col_for_para].loc[gdf[group] == select.value],
            gdf.loc[gdf[group] == default],
            sliders,
            select.value,
            min_iso,
            max_iso
            )

#Widgets
# HOVER TOOL
hover = HoverTool(
        tooltips=tooltips,
        names = ["buildings"]
        )
map_.add_tools(hover)


#Change angles max value
sliders["angles"].value = (0,angles_value_max_base)

widgetbox(
        [x for x in sliders.values()]
    )
button.on_click(update)
reset_button.on_click(reset)
widgets = [select, radio_group]
widgets.extend([x for x in sliders.values()])
widgets.extend([button, reset_button])
widgets_map = [
                color_picker_iso,
                back_slider,
                iso_alpha_slider,
                iso_progression_slider
                ]

#Panels and tabs
tab_map = Panel(
        child=row(
            [
                map_, 
                Spacer(width=50),
                widgetbox(widgets_map)
                ]
            ),
        title="Map"
        )
tab_global = Panel(
        child=column([hist, para]),
        title="Synthesis"
        )
tab_tables = Panel(
        child=data_table,
        title="Datatables"
        )
tabs = Tabs(tabs=[tab_map, tab_tables, tab_global])

#Layout
layout = row(
        widgetbox(widgets),
        Spacer(width=50),
        tabs
        )

curdoc().add_root(layout)