## Presentation

This docker (*based as the others on geodecision package*):
* makes automatic classifications for socio-economic data
* returns Geopackage or GeoJSON classified spatial data

> ***/!\ WARNING: could take a long time (2mns/variable)***

## Methodological approach
Let explain by using an example: INSEE gridded data (*we use the gridded data (200m) FiLoSoFi in this docker*).

| Name | Provider | License & terms of use | Warnings | Documentation | Variables |
|:-----|:---------|:-----------------------|:---------|:--------------|:----------|
| [Gridded data (*1km*) FiLoSoFi](https://www.insee.fr/fr/statistiques/4176293?sommaire=4176305#consulter-sommaire) | [INSEE](https://www.insee.fr/en/) | [Link](https://statistiques-locales.insee.fr/#c=contact) | [INSEE Warnings (*fr*)](https://statistiques-locales.insee.fr/#c=article) | [Link](https://www.insee.fr/fr/statistiques/4176293?sommaire=4176305#documentation) | [Dictionary of variables](https://www.insee.fr/fr/statistiques/4176293?sommaire=4176305#documentation) |
| [Gridded data (*200m*) FiLoSoFi](https://www.insee.fr/fr/statistiques/4176290?sommaire=4176305#consulter) | [INSEE](https://www.insee.fr/en/) | [Link](https://statistiques-locales.insee.fr/#c=contact) | [INSEE Warnings (*fr*)](https://statistiques-locales.insee.fr/#c=article) | [Link](https://www.insee.fr/fr/statistiques/4176290?sommaire=4176305#documentation) | [Dictionary of variables](https://www.insee.fr/fr/statistiques/4176290?sommaire=4176305#dictionnaire) |


## Configuration table
> *This table explains the ```config.json``` file*. It contains list of settings (*because the ClassificationDataFrames from geodecision can loop on multiple variables and files*). The table shows a typical element of a list.

"name": "INSEE_gridded_data_200m",
"filepath": "./data/INSEE/Filosofi_2015_Lyon_Villeurbanne_200m_grid.geojson",
"output_dir": "outputs",
"driver": "GPKG",

| name | type | description | example |
|:-----|:----:|:------------|:-------:|
| ***name*** | str | name of the element & output name | *"INSEE_gridded_data_200m"*|
| ***filepath*** | str | Input GeoJSON filepath | *"./data/INSEE/Filosofi_2015_Lyon_Villeurbanne_200m_grid.geojson"*|
| ***output_dir*** | str | Output directory | *"outputs"*|
| ***driver*** | int | Driver for output (*"GPKG" or "GeoJSON"*) | *"GPKG"*|
| ***variables*** | dict | Dictionary of variables (*see [Variables](#variables) section below for a detailed example*). Each variable contains a boolean for classification (*if needed or not*) and a description, *see [below](#variable_structure_detailed_explanations)*) | ```"Ind": {"classification": true, "description": "Nombre d’individus"}``` |

### Variable structure detailed explanations
The module ```classification``` (*in geodecision*) is based on the ```mapclassify``` from Pysal.

* [References](https://pysal.org/mapclassify/references.html)
* [Automatic classification](https://pysal.org/mapclassify/generated/mapclassify.KClassifiers.html)

This module allows to measure and determine the best classification and make classes for our data.

This module requires a JSON parameters file as input (*with the structure illustrated below*)

```json
[{
                "name": "name of the futur GeoDataFrame A",
                "filepath": "path/to/GeoJSON file",
                "output_dir": "outputs",
                "dirver":"GPKG",
                "variables": {
                    "variable 1": {
                        "classification": boolean (if true, make classification, else set to false),
                        "description": "Short description of the var"
                    },
                    "variable 2": {
                        "classification": boolean (if true, make classification, else set to false),
                        "description": "Short description of the var"
                },
                {
                    "name": "name of the futur GeoDataFrame A",
                    "filepath": "path/to/GeoJSON file",
                    "output_dir": "outputs",
                    "dirver":"GPKG",
                    "variables": {
                        "variable 1": {
                            "classification": boolean (if true, make classification, else set to false),
                            "description": "Short description of the var"
                        },
                        "variable 2": {
                            "classification": boolean (if true, make classification, else set to false),
                            "description": "Short description of the var"
                        }
                    }
                }
            ]
```

#### [Variables](https://www.insee.fr/fr/statistiques/4176290?sommaire=4176305#dictionnaire)
| Field | Details |
|:------|:--------|
| IdINSPIRE |  Identifiant Inspire du carreau de 200 m |
| I_est_cr | Vaut 1 si le carreau de 200 m est imputé par une valeur approchée, 0 sinon |
| Id_carr_n | Identifiant Inspire du carreau de niveau naturel auquel appartient le carreau de 200 m |
| Groupe | Numéro du groupe auquel appartient le carreau (*voir [documentation](https://www.insee.fr/fr/statistiques/4176290?sommaire=4176305#doc)*) |
| Depcom | Code commune, selon le code officiel géographique 2019, auquel sont rattachés la majorité des ménages du carreau |
| Id_car2010 | Identifiant Inspire du carreau de 200 m figurant dans la base de données carroyées à 200 m diffusée avec la source RFL2010 (*le nombre de caractères peut être différent de celui de IdINSPIRE*) |
| Id_carr1km | Identifiant Inspire du carreau de 1 km auquel appartient le carreau de 200 m |
| I_pauv | Nombre de carreaux de 200 m compris dans le carreau de 1 km qui ont été traités pour respecter la confidentialité sur le nombre de ménages pauvres |
| I_est_1km | Vaut 1 si le carreau est imputé par une valeur approchée, 0 ou 2 sinon |
| Ind | Nombre d’individus |
| Men | Nombre de ménages |
| Men_pauv | Nombre de ménages pauvres |
| Men_1ind | Nombre de ménages d’un seul individu |
| Men_5ind | Nombre de ménages de 5 individus ou plus |
| Men_prop | Nombre de ménages propriétaires |
| Men_fmp | Nombre de ménages monoparentaux |
| Ind_snv | Somme des niveaux de vie winsorisés des individus |
| Men_surf | Somme de la surface des logements du carreau |
| Men_coll | Nombre de ménages en logements collectifs |
| Men_mais | Nombre de ménages en maison |
| Log_av45 | Nombre de logements construits avant 1945 |
| Log_45_70 | Nombre de logements construits entre 1945 et 1969 |
| Log_70_90 | Nombre de logements construits entre 1970 et 1989 |
| Log_ap90 | Nombre de logements construits depuis 1990 |
| Log_inc | Nombre de logements dont la date de construction est inconnue |
| Log_soc | Nombre de logements sociaux |
| Ind_0_3 | Nombre d’individus de 0 à 3 ans |
| Ind_4_5 | Nombre d’individus de 4 à 5 ans |
| Ind_6_10 | Nombre d’individus de 6 à 10 ans |
| Ind_11_17 | Nombre d’individus de 11 à 17 ans |
| Ind_18_24 | Nombre d’individus de 18 à 24 ans |
| Ind_25_39 | Nombre d’individus de 25 à 39 ans |
| Ind_40_54 | Nombre d’individus de 40 à 54 ans |
| Ind_55_64 | Nombre d’individus de 55 à 64 ans |
| Ind_65_79 | Nombre d’individus de 65 à 79 ans |
| Ind_80p | Nombre d’individus de 80 ans ou plus |
| Ind_inc | Nombre d’individus dont l’âge est inconnu |

## Inputs/Outputs
* **Input**:
    * GeoJSON file(s) with socio-economic data
    * ```config.json```:
        * *example*:
            ```JSON
            [{
                "name": "INSEE_gridded_data_200m",
                "filepath": "./data/INSEE/Filosofi_2015_Lyon_Villeurbanne_200m_grid.geojson",
                "output_dir": "outputs",
                "driver": "GPKG",
                "variables": {
                    "Id_carr1km": {
                        "classification": false,
                        "description": "Identifiant Inspire du carreau de 1 km"
                    },
                    "Ind": {
                        "classification": true,
                        "description": "Nombre d’individus"
                    },
                    "Men": {
                        "classification": true,
                        "description": "Nombre de ménages"
                    },
                    "Men_pauv": {
                        "classification": true,
                        "description": "Nombre de ménages pauvres"
                    },
                    "Ind_snv": {
                        "classification": true,
                        "description": "Somme des niveaux de vie winsorisés des individus"
                    },
                    "Men_surf": {
                        "classification": false,
                        "description": "Somme de la surface des logements du carreau"
                    },
                    "Men_coll": {
                        "classification": true,
                        "description": "Nombre de ménages en logements collectifs"
                    },
                    "Men_mais": {
                        "classification": true,
                        "description": "Nombre de ménages en maison"
                    },
                    "Log_av45": {
                        "classification": true,
                        "description": "Nombre de logements construits avant 1945"
                    },
                    "Log_45_70": {
                        "classification": true,
                        "description": "Nombre de logements construits entre 1945 et 1969"
                    },
                    },
                    "IdINSPIRE": {
                        "classification": false,
                        "description": ""
                    }
                }
            }]

            ```

* **Outputs**:
    * geospatial files with classification (*GeoJSON, Geopackage*)
    * ```classifications.log``` file containing:
        * classification duration for each variable
        * best classification method
        * all the tested classifications with bins and counts (*to check the tested ones with the best one*)

## Build
> *following command works inside the Dashboard/DockerContext directory*

```bash
sudo docker build --build-arg git_token=<TOKEN> -t classification <DockerContext>
```

## Run
> *following command works inside the Dashboard/ directory*

```bash
sudo docker run --mount src=`pwd`,target=/Input,type=bind --mount src=`pwd`,target=/Output,type=bind -it classification
```
