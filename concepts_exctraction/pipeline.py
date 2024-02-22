"""
This is a boilerplate pipeline 'concepts_exctraction'
generated using Kedro 0.18.2
"""

from .nodes import extract_concepts, filter_mentions_df_type, filter_mentions_df_confidence

from .nodes import enhance_mentions_df, filter_mentions_df_multiple_occ, filter_mentions_df_conceptnet

from .nodes import generate_files_mentions_df_concept_list



from kedro.pipeline import Pipeline, node, pipeline


def create_pipeline(**kwargs) -> Pipeline:
    """node(
            func=extract_concepts,
            inputs="text_df",
            outputs=["mentions_df_raw", "text_df_final"],
            name="node_extract_concepts"
            ),
    """
    return pipeline([
        node(
            func=extract_concepts,
            inputs="text_df",
            outputs=["mentions_df_raw", "text_df_final"],
            name="node_extract_concepts"
            ),
        node(
            func=filter_mentions_df_type,
            inputs="mentions_df_raw",
            outputs="mentions_df_filtered_type",
            name="node_filter_by_type"
            ),
        node(
            func=filter_mentions_df_confidence,
            inputs="mentions_df_filtered_type",
            outputs="mentions_df_filtered_confidence",
            name="node_filter_by_confidence"
            ),
        node(
            func=enhance_mentions_df,
            inputs=["mentions_df_filtered_confidence", "text_df"],
            outputs="mentions_df_enhanced",
            name="node_enhance_mentions_df"
            ),
        node(
            func=filter_mentions_df_multiple_occ,
            inputs="mentions_df_enhanced",
            outputs="mentions_df_filtered_multiple_occurrences",
            name="node_filter_by_multiple_occ"
            ),
        node(
            func=filter_mentions_df_conceptnet,
        inputs=["mentions_df_filtered_multiple_occurrences", "dbpedia_to_conceptnet_prev", "conceptnet_to_dbpedia_prev"],
            outputs=["mentions_df_filtered_conceptnet", "dbpedia_to_conceptnet", "conceptnet_to_dbpedia"],
            name="node_filter_by_conceptnet"
            ),
        node(
            func=generate_files_mentions_df_concept_list,
            inputs="mentions_df_filtered_conceptnet",
        outputs=["mentions_df_final", "concepts_list", "concepts_list_final"],
            name="node_generate_files_mentions_df_concept_list"
            ),
        ])

