"""
This is a boilerplate pipeline 'concepts_nodes_info'
generated using Kedro 0.18.2
"""

from SPARQLWrapper import SPARQLWrapper, JSON, N3

import pandas as pd
import traceback
import logging

import json

def execute_sparql_queries(concepts_list:list, concepts_data_list_prev:list):

	def get_sparql_basic_info(sparql, concept):

		print(concept)
		sparql.setQuery(f'''
		SELECT ?name ?comment
		WHERE {{ {concept} rdfs:label ?name.
			{concept} rdfs:comment ?comment.
		
			FILTER (lang(?name) = 'en')
			FILTER (lang(?comment) = 'en')
		}}''')

		rdf:type

		sparql.setReturnFormat(JSON)
		qres = sparql.query().convert()
		
		try:
			result = qres['results']['bindings'][0]
		
			name = result['name']['value'] 
			comment = result['comment']['value']

			return name, comment
			
		except IndexError:
			pass
		
		return "", ""

		
	def get_sparql_image(sparql, concept):


		sparql.setQuery(f'''
		SELECT ?image 
		WHERE {{ {concept} dbo:thumbnail ?image.
		
		}}''')

		sparql.setReturnFormat(JSON)
		qres = sparql.query().convert()
		
		try:
			result = qres['results']['bindings'][0]
			image_url = result['image']['value']
			return image_url
		except IndexError:
			pass
		return ""


	def get_sparql_related_from(sparql, concept):

		
		sparql.setQuery(f'''
		CONSTRUCT {{ {concept} dct:subject ?subject.
			{concept} dbo:wikiPageWikiLink ?related_entities_from.
			{concept} rdf:type ?types .}}''' +
		f'''
		WHERE {{{{ {concept} dct:subject ?subject . }} UNION {{{concept} dbo:wikiPageWikiLink ?related_entities_from . }} UNION {{{concept} rdf:type ?types . }} }}''')


		sparql.setReturnFormat(JSON)
		qres = sparql.query().convert()

		types_list = []
		subject_list = []
		related_entities_from = []
		
		for result in qres['results']['bindings']:

			if result['p']['value'] == 'http://dbpedia.org/ontology/wikiPageWikiLink':
				ent = result['o']['value']
				if ".jpg" not in ent:
					related_entities_from.append(ent)

			elif result['p']['value'] == 'http://purl.org/dc/terms/subject':
				subject = result['o']['value']
				if ".jpg" not in subject:
					subject_list.append(subject)
			
			elif result['p']['value'] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
				types = result['o']['value']
				if ".jpg" not in types:
					types_list.append(types)

		return types_list, subject_list, related_entities_from


	def get_sparql_related_to(sparql, concept):

		sparql.setQuery(f'''
		CONSTRUCT {{ ?related_entities_to dbo:wikiPageWikiLink {concept} .}}''' +
		f''' 
		WHERE {{ ?related_entities_to dbo:wikiPageWikiLink {concept} . }}''')


		sparql.setReturnFormat(JSON)
		qres = sparql.query().convert()

		related_entities_to = []

		for result in qres['results']['bindings']:

			if result['p']['value'] == 'http://dbpedia.org/ontology/wikiPageWikiLink':
				ent = result['s']['value']
				if ".jpg" not in ent:
					related_entities_to.append(ent)
		
		return related_entities_to


	def run_sparql_queries_for_concept(sparql, concept_url):

		dbpedia_url = concept_url

		concept_url = "<" + concept_url + ">"
		name, comment = get_sparql_basic_info(sparql, concept_url)


		try:
			if name == "":
				print("Query failed to run for entity: ", concept_url)
				return None

			else:
			
				print(name)
				#print(comment)

				image_url = get_sparql_image(sparql, concept_url)

				types_list, subject_list, related_entities_from = get_sparql_related_from(sparql, concept_url)

				related_entities_to = get_sparql_related_to(sparql, concept_url)

				subject_of, narrower_categories, broader_categories = [], [], []

				concept_data = [dbpedia_url, name, comment, image_url, types_list, subject_list, related_entities_from, related_entities_to, subject_of, narrower_categories, broader_categories]
				
				
			return concept_data
		except Exception as e:
			return None
			pass

	new_concepts_data_list = []
	for data in concepts_data_list_prev:
		if type(data) != type([0]):
			print("Error")
			print(data)
		else:
			new_concepts_data_list.append(data)

	concepts_data_list = new_concepts_data_list

	column_names = ["DBpedia URL", "Name", "Abstract", "Image", "DBpedia Types", "Subject FROM", "Related Entities FROM", "Related Entities OF", "Subject OF", "Narrower Categories", "Broader Categories"] 

	concepts_df = pd.DataFrame(concepts_data_list, columns=column_names)
	

	sparql = SPARQLWrapper('https://dbpedia.org/sparql')


	count = 0

	for concept in concepts_list:
		print(count)
		count+=1
		if concept not in list(concepts_df["DBpedia URL"]):
        		concept_data = run_sparql_queries_for_concept(sparql, concept)
	        	print(concept, " fetching data for the concept.")
		        concepts_data_list.append(concept_data)
		else:
        		print(concept, " already in the database...")
		
		
		with open("Temporary_concepts_data_list.json", "w") as f:
			json.dump(concepts_data_list, f)
			
	print("0")
	concepts_data_list = list(concepts_data_list)

	new_concepts_data_list = []
	for item in concepts_data_list:
		if item != None:
			new_concepts_data_list.append(item)
	
	concepts_data_list = list(new_concepts_data_list)

	print("1")

	column_names = ["DBpedia URL", "Name", "Abstract", "Image", "DBpedia Types", "Subject FROM", "Related Entities FROM", "Related Entities OF", "Subject OF", "Narrower Categories", "Broader Categories"] 
	print("2")
	concept_df = pd.DataFrame(concepts_data_list, columns=column_names)
	print("3")
	concepts_database = concept_df[concept_df["DBpedia URL"].isin(concepts_list)]
	print("4")
	
	return concepts_database, concepts_data_list


#	return concepts_data_list


#def create_concepts_database(concepts_list: list, concepts_data_list: list) -> pd.DataFrame:

	

