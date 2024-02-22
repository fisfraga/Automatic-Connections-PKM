"""
This is a boilerplate pipeline 'concepts_relation_info'
generated using Kedro 0.18.2
"""

from .nodes import build_relatedness_matrix_dict, build_relations_dict, enhance_concepts_database, build_relatedness_matrix_dict_NO_OUTPUT

from kedro.pipeline import Pipeline, node, pipeline


def create_pipeline(**kwargs) -> Pipeline:
    """
    node(
            func=build_relatedness_matrix_dict,
            inputs=["concepts_list", "dbpedia_to_conceptnet", "conceptnet_distances_dict_prev"],
            outputs="conceptnet_distances_dict",
            name="node_build_relatedness_matrix_dict"
            ),

    OR
    
    node(
            func=build_relatedness_matrix_dict_NO_OUTPUT,
            inputs=["concepts_list", "dbpedia_to_conceptnet", "conceptnet_distances_dict_prev"],
            outputs="conceptnet_distances_dict",
            name="node_build_relatedness_matrix_dict"
            ),
    """
    return pipeline([

        node(
            func=build_relatedness_matrix_dict,
            inputs=["concepts_list", "dbpedia_to_conceptnet", "conceptnet_distances_dict_prev"],
            outputs="conceptnet_distances_dict",
            name="node_build_relatedness_matrix_dict"
            ),
        node(
            func=build_relations_dict,
            inputs=["concepts_list", "dbpedia_to_conceptnet", "conceptnet_relations_list", "conceptnet_relations_dict_prev"],
            outputs="conceptnet_relations_dict",
            name="node_build_relations_dict"
            ),
        node(
            func=enhance_concepts_database,
            inputs=["concepts_database", "conceptnet_distances_dict", "conceptnet_relations_dict"],
            outputs="concepts_database_enhanced",
            name="node_enhance_concepts_database"
            ),
        ])
