import argparse
import os
from mapactionpy_controller.event import Event
from mapactionpy_controller.map_recipe import MapRecipe
from mapactionpy_controller.layer_properties import LayerProperties
from arcpro_runner import ArcProRunner


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error('The file "%s" does not exist!' % arg)
    else:
        return arg


def main(args):
    args = parser.parse_args()
    event = Event(args.eventDescriptionFile)
    runner = ArcProRunner(event)

    recipe_without_positive_iso3_code = (
        '''{
            "mapnumber": "MA001",
            "category": "Reference",
            "product": "DJI Overview Map",
            "summary": "Overview of DJI with topography displayed",
            "export": true,
            "template": "reference",
            "map_frames": [
                {
                    "name": "Main map",
                    "layers": [
                        {
                            "name": "mainmap-stle-stl-pt-s0-allmaps",
                            "reg_exp": "^dji_stle_stl_pt_(.*?)_(.*?)_([phm][phm])(.*?).shp$",
                            "schema_definition": "stle_ste_pt.yml",
                            "definition_query": "fclass IN ('national_capital', 'city', 'capital', 'town')",
                            "display": true,
                            "add_to_legend": true,
                            "label_classes": [
                                {
                                    "class_name": "National Capital",
                                    "expression": "[name]",
                                    "sql_query": "('fclass' = 'national_capital')",
                                    "show_class_labels": true
                                },
                                {
                                    "class_name": "Admin 1 Capital",
                                    "expression": "[name]",
                                    "sql_query": "('fclass' = 'town')",
                                    "show_class_labels": true
                                }
                            ]
                        }
                    ]
                }
            ]
        }'''
    )

    layerProperties = LayerProperties(event.cmf_descriptor_path, '.lyr', verify_on_creation=False)
    recipe = MapRecipe(recipe_without_positive_iso3_code, layerProperties)
    recipe = runner.get_templates(state=recipe)
    recipe = runner.create_ouput_map_project(state=recipe)
    recipe = runner.build_project_files(state=recipe)
    recipe = runner.export_maps(state=recipe)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Executes ArcProRunner for a given event',
    )
    parser.add_argument("--event", dest="eventDescriptionFile", required=True,
                        help="path to file", metavar="FILE", type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    main(args)
