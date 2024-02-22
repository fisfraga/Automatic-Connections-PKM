"""
This is a boilerplate pipeline 'concepts_nodes_info'
generated using Kedro 0.18.2
"""

from .nodes import execute_sparql_queries#, create_concepts_database

from kedro.pipeline import Pipeline, node, pipeline


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=execute_sparql_queries,
            inputs=["concepts_list", "concepts_data_list_prev"],
            outputs=["concepts_database", "concepts_data_list"],
            name="node_execute_sparql_queries"
            ),



        ])


"""
        node(
            func=execute_sparql_queries,
            inputs=["concepts_list", "concepts_data_list_prev"],
            outputs=["concepts_data_list"],
            name="node_execute_sparql_queries"
            ),
        node(
            func=create_concepts_database,
            inputs=["concepts_list", "concepts_data_list"],
            outputs="concepts_database",
            name="node_create_concepts_database"
            ),
"""