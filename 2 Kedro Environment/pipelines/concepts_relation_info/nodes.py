"""
This is a boilerplate pipeline 'concepts_relation_info'
generated using Kedro 0.18.2
"""


import pandas as pd

import json

import requests


def build_relatedness_matrix_dict_NO_OUTPUT(concepts_list:list, dbpedia_to_conceptnet:dict, conceptnet_distances_dict_prev:dict) -> dict:
	
	conceptnet_distances_dict = conceptnet_distances_dict_prev

	no_concept_net_entry = []

	for keyy in dbpedia_to_conceptnet.keys():
		item = dbpedia_to_conceptnet[keyy]
		if item == "":
			no_concept_net_entry.append(item)

	i=0

	for concept_url in concepts_list:


		main_dict_keys = list(conceptnet_distances_dict.keys())
		

		if concept_url in main_dict_keys:
			inner_dict_keys = list(conceptnet_distances_dict[concept_url].keys())
			print(i, "Concept already exists in Dict: ", concept_url)
		else:
			conceptnet_distances_dict[concept_url] = {}
			inner_dict_keys=[]

		concept = dbpedia_to_conceptnet[concept_url]


		print("Fetching Similarities ... ", i, " .... Concept: ", concept)
	
		j=0 

		for concept_url_2 in concepts_list:
			if i == j:
				score = 1
			elif concept_url_2 in no_concept_net_entry or concept_url in no_concept_net_entry:
				score = 0
		
			elif i<j:
				
				concept2 = dbpedia_to_conceptnet[concept_url_2]
			
				if concept_url_2 in inner_dict_keys:
			
					score = conceptnet_distances_dict[concept_url][concept_url_2]
					if score == 0:
						print(j, " Score zerado para: ", concept, " e ", concept2)

						try:

							query_url = "http://api.conceptnet.io/relatedness?node1=" + concept + "&node2=" + concept2 + "&limit=10"

							response = requests.get(query_url)
							obj = response.json()
							score = obj['value']
						except:
							print("Deu RUIM de verdade, Score continua ZERADO : ", concept, " and ", concept2)
							score = -50
					
				"""
				else:
					try:

						query_url = "http://api.conceptnet.io/relatedness?node1=" + concept + "&node2=" + concept2 + "&limit=10"

						response = requests.get(query_url)
						obj = response.json()
						score = obj['value']
					except:
						print("Failed finding similarity between: ", concept, " and ", concept2)
						score = -50
				"""		

			elif concept_url_2 in main_dict_keys:

				score = conceptnet_distances_dict[concept_url_2][concept_url]
				concept2 = dbpedia_to_conceptnet[concept_url_2]
				if score == -50:
					print(j, " Score zerado (2) para: ", concept, " e ", concept2)

					try:

						query_url = "http://api.conceptnet.io/relatedness?node1=" + concept + "&node2=" + concept2 + "&limit=10"

						response = requests.get(query_url)
						obj = response.json()
						score = obj['value']
					except:
						print("Deu RUIM de verdade, Score continua ZERADO : ", concept, " and ", concept2)
						score = -50
				
			else:
				print("ALGO DEU ERRADO. Ou na real: tudo foi pulado lindamente")
				score = 0

			conceptnet_distances_dict[concept_url][concept_url_2] = score

			j += 1	

		i +=1
		
		#with open("Temporary_conceptnet_distances_dict.json", "w") as f:
		#	json.dump(conceptnet_distances_dict, f)

	return conceptnet_distances_dict


def build_relatedness_matrix_dict(concepts_list:list, dbpedia_to_conceptnet:dict, conceptnet_distances_dict_prev:dict) -> dict:
	
	conceptnet_distances_dict = conceptnet_distances_dict_prev

	no_concept_net_entry = []

	for keyy in dbpedia_to_conceptnet.keys():
		item = dbpedia_to_conceptnet[keyy]
		if item == "":
			no_concept_net_entry.append(item)

	i=0

	for concept_url in concepts_list:


		main_dict_keys = list(conceptnet_distances_dict.keys())
		

		if concept_url in main_dict_keys:
			inner_dict_keys = list(conceptnet_distances_dict[concept_url].keys())
			print(i, "Concept already exists in Dict: ", concept_url)
		else:
			conceptnet_distances_dict[concept_url] = {}
			inner_dict_keys=[]

		concept = dbpedia_to_conceptnet[concept_url]


		print("Fetching Similarities ... ", i, " .... Concept: ", concept)
	
		j=0 

		for concept_url_2 in concepts_list:
			if i == j:
				score = 1
			elif concept_url_2 in no_concept_net_entry or concept_url in no_concept_net_entry:
				score = 0
		
			elif i<j:
				
				concept2 = dbpedia_to_conceptnet[concept_url_2]
			
				if concept_url_2 in inner_dict_keys:
			
					score = conceptnet_distances_dict[concept_url][concept_url_2]
					if score == 0:
						print(j, " Score zerado para: ", concept, " e ", concept2)

						try:

							query_url = "http://api.conceptnet.io/relatedness?node1=" + concept + "&node2=" + concept2 + "&limit=10"

							response = requests.get(query_url)
							obj = response.json()
							score = obj['value']
						except:
							print("Deu RUIM de verdade, Score continua ZERADO : ", concept, " and ", concept2)
							score = -50
					
				else:
					try:

						query_url = "http://api.conceptnet.io/relatedness?node1=" + concept + "&node2=" + concept2 + "&limit=10"

						response = requests.get(query_url)
						obj = response.json()
						score = obj['value']
					except:
						print("Failed finding similarity between: ", concept, " and ", concept2)
						score = -50
							

			elif concept_url_2 in main_dict_keys:

				score = conceptnet_distances_dict[concept_url_2][concept_url]
				concept2 = dbpedia_to_conceptnet[concept_url_2]
				if score == -50:
					print(j, " Score zerado (2) para: ", concept, " e ", concept2)

					try:

						query_url = "http://api.conceptnet.io/relatedness?node1=" + concept + "&node2=" + concept2 + "&limit=10"

						response = requests.get(query_url)
						obj = response.json()
						score = obj['value']
					except:
						print("Deu RUIM de verdade, Score continua ZERADO : ", concept, " and ", concept2)
						score = -50
				
			else:
				print("ALGO DEU ERRADO.")
				score = 0

			conceptnet_distances_dict[concept_url][concept_url_2] = score

			j += 1	

		i +=1
		
		#with open("Temporary_conceptnet_distances_dict.json", "w") as f:
		#	json.dump(conceptnet_distances_dict, f)

	return conceptnet_distances_dict



def build_relations_dict(concepts_list:list, dbpedia_to_conceptnet:dict, conceptnet_relations_list:list, conceptnet_relations_dict_prev:dict) -> dict:

	no_concept_net_entry = []

	for keyy in dbpedia_to_conceptnet.keys():
		item = dbpedia_to_conceptnet[keyy]
		if item == "":
			no_concept_net_entry.append(item)
	
	i=0
	
	conceptnet_relations_dict = conceptnet_relations_dict_prev

	for concept_url in concepts_list:

		if concept_url not in conceptnet_relations_dict.keys():

			if concept_url in no_concept_net_entry:
				print(i, "   -   Following Concept not in ConceptNet: ", concept_url)
				for relation in conceptnet_relations_list:
					conceptnet_relations_dict[concept_url][relation] = []
			else:
				conceptnet_relations_dict[concept_url] = {}
				inner_dict_keys=[]

				concept = dbpedia_to_conceptnet[concept_url]

				print(i, "   -   Fetching data for concept: ", concept)
				
				for relation in conceptnet_relations_list:
					try:
						query_url = "http://api.conceptnet.io/query?start=" + concept + "&rel=" + relation  + "&other=/c/en&limit=100"
						response = requests.get(query_url)
						obj = response.json()
						related_concepts = [edge['end']['@id'] for edge in obj['edges']]
					except:
						print(i, " Deu RUIM para o conceito : ", concept, " e relation: ", relation)
								
						related_concepts = [0]
						
					conceptnet_relations_dict[concept_url][relation] = related_concepts
			

		i += 1

	return conceptnet_relations_dict


def enhance_concepts_database(concepts_database: pd.DataFrame, conceptnet_distances_dict:dict, conceptnet_relations_dict:dict)->pd.DataFrame:

	#distances_dict_column = []

	relations_dict_column = []

	for row in concepts_database.itertuples():

		concept_id = row[1]

		#distances_dict = conceptnet_distances_dict[concept_id]

		relations_dict = conceptnet_relations_dict[concept_id]

		#distances_dict_column.append(distances_dict)

		relations_dict_column.append(relations_dict)

	concepts_database_enhanced = concepts_database.copy()

	#concepts_database_enhanced['ConceptNet_Distances'] = distances_dict_column

	concepts_database_enhanced['ConceptNet_Relations'] = relations_dict_column

	return concepts_database_enhanced


