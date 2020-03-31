#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 18:12:36 2020

@author: thomas
"""

from shapely.geometry import Polygon
                 
def set_para(gdf, selection, sliders, layer, min_iso, max_iso):

    selection["geometry"] = selection["geometry"].map(
        lambda x: Polygon(x)
        )
    str_ = """
             <!DOCTYPE html>
            <html>
            <head>
            <style>
            table {
              border-collapse: collapse;
              width: 100%;
            }
            
            th, td {
              text-align: left;
              padding: 7px;
              font-size:12px
            }
            
            tr:nth-child(even) {background-color: #7ec8ffff;}
            </style>
            </head>
            <body>
            """
            
    str_ += """
            <h4>Synthesis for layer {} rooftops polygons</h4>
            <table>
            """.format(layer)
            
    nb_roofs = len(selection)
    
    str_ += """
            <tr>
              <th></th>
              <th></th>
              <th>ALL</th>
              <th><b>IN (iso)</b></th>
              <th><b>OUT (iso)</b></th>
            </tr>
            """
    for k,v in sliders.items():
        selected = gdf.loc[
            (gdf[k] >= v.value[0]) 
            & (gdf[k] < v.value[1])
            ]
        if min_iso == "0": 
            select_inside = gdf[k].loc[
                (gdf[k] >= v.value[0]) 
                & (gdf[k] < v.value[1])
                & (gdf[max_iso]) == True
                ]
            select_outside = gdf[k].loc[
                (gdf[k] >= v.value[0]) 
                & (gdf[k] < v.value[1])
                &(gdf[max_iso]) == False
                ]
        else:
            select_inside = gdf[k].loc[
                (gdf[k] >= v.value[0]) 
                & (gdf[k] < v.value[1])
                &(gdf[min_iso]) == True
                &(gdf[max_iso]) == True
                ]
            select_outside = gdf[k].loc[
                (gdf[k] >= v.value[0]) 
                & (gdf[k] < v.value[1])
                &(gdf[min_iso]) == False
                &(gdf[max_iso]) == False
                ]
        str_ += """
                <tr>
                  <th>% of rooftops filtered by <i>{}</i></th>
                  <th>{} <= x < {}</th>
                  <th><b>{} %</b></th>
                  <th><b>{} %</b></th>
                  <th><b>{} %</b></th>
                </tr>
                """.format(
                k,
                round(v.value[0]),
                round(v.value[1]),
                round(len(selected) / nb_roofs * 100),
                round(len(select_inside) / nb_roofs * 100),
                round(len(select_outside) / nb_roofs * 100)
                )
    
    if min_iso == "0": 
        selection_inside = gdf.loc[gdf[max_iso] == True]
        selection_outside = gdf.loc[gdf[max_iso] == False]
    else:
        selection_inside = gdf.loc[
            (gdf[min_iso] == True) 
            & (gdf[max_iso] == True)
            ]
        selection_outside = gdf.loc[
            (gdf[min_iso] == False) 
            & (gdf[max_iso] == False)
            ]
                                
    str_ += """
             <tr>
                  <th>Number of filtered roofs</th>
                  <th></th>
                  <td><b>{}</b></td>
                  <td><b>{}</b></td>
                  <td><b>{}</b></td>
                  
             </tr>
            """.format(
            len(selection),
            len(selection_inside),
            len(selection_outside)
            )
    str_ += """
             <tr>
                  <th>Total number of layer's rooftops</th>
                  <th></th>
                  <td><b>{}</b></td>
             </tr>
            """.format(
            nb_roofs
            )
    str_ += """
             <tr>
                  <th>% of rooftops with potential</th>
                  <th></th>
                  <td><b>{}%</b></td>
                  <td><b>{}%</b></td>
                  <td><b>{}%</b></td>
             </tr>
            """.format(
            round(len(selection) / nb_roofs * 100),
            round(len(selection_inside) / nb_roofs * 100),
            round(len(selection_outside) / nb_roofs * 100) 
            )
    str_ += """
             <tr>
                  <th>Total rooftops area (m²)</th>
                  <th></th>
                  <td><b>{}</b></td>
             </tr>
            """.format(
            round(gdf.area.sum())  
            )

    str_ += """
             <tr>
                  <th>Rooftops area with potential (m²)</th>
                  <th></th>
                  <td><b>{}</b></td>
                  <td><b>{}</b></td>
                  <td><b>{}</b></td>
             </tr>
            """.format(
            round(selection.area.sum()),
            round(selection_inside.area.sum()),
            round(selection_outside.area.sum())
            )
    str_ += """
             <tr>
                  <th>% of potential rooftops area</th>
                  <th></th>
                  <td><b>{}%</b></td>
                  <td><b>{}%</b></td>
                  <td><b>{}%</b></td>
             </tr>
            """.format(
            round(selection["area"].sum()/gdf["area"].sum() * 100),
            round(selection_inside.area.sum()/gdf.area.sum() * 100),
            round(selection_outside.area.sum()/gdf.area.sum() * 100) 
            )
    str_ += """
            </table>
            </body>
            </htlm>
            """
    return str_