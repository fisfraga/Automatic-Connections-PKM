"""
This is a boilerplate pipeline 'semantic_relatedness'
generated using Kedro 0.18.2
"""

from .nodes import create_distance_matrixes

from kedro.pipeline import Pipeline, node, pipeline


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=create_distance_matrixes,
            inputs=["text_df","sentence_transformer_model_list"],
            outputs="relatedness_df",
            name="node_create_distance_matrixes"
            ),
        ])

