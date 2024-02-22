"""
This is a boilerplate pipeline 'semantic_relatedness'
generated using Kedro 0.18.2
"""

import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer, util
import torch

import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'

def create_distance_matrixes(text_df:pd.DataFrame, sentence_transformer_model_list:list) -> pd.DataFrame:

	def create_result_column(model, text_df, corpus, corpus_embeddings, query):

		query_embeddings = model.encode(query, convert_to_tensor=True)

		results = util.semantic_search(query_embeddings, corpus_embeddings, top_k=len(corpus), score_function=util.cos_sim)

		results_dict = {}
		for result in results[0]:
			id = text_df.iloc[result['corpus_id'],4]
			score = result['score']
			results_dict[id] = round(score, 5)
		
		result_column = []
		for id in text_df.index:
			result_column.append(results_dict[id])

		return result_column


	model = SentenceTransformer(sentence_transformer_model_list[0]) # Pega o primeiro modelo da lista 
	print("Model loaded.")
	relatedness_df = text_df[["Text_ID", "Father_ID", "Father_name", "Author_name", "Text"]]

	corpus = list(text_df["Text"])
	corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

	print("Embeddings Generated.")
	relatedness_dict = {}

	for row in text_df.itertuples():
		column_name = row[0]
		query = row[4]

		new_column = create_result_column(model, text_df, corpus, corpus_embeddings, query)
		relatedness_dict[column_name] = new_column

	for keyy in relatedness_dict.keys():
		relatedness_df[keyy] = relatedness_dict[keyy]

	return relatedness_df



