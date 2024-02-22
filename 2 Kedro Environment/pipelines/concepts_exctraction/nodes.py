"""

Concepts Extraction

This is a boilerplate pipeline 'concepts_exctraction'
generated using Kedro 0.18.2
"""


import pandas as pd

import spacy
import spacy_dbpedia_spotlight


from dandelion import default_config
from dandelion import DataTXT

import requests


def extract_concepts(text_df: pd.DataFrame):

	def get_dande_entities_dict(text, datatxt):

		try:

			response = datatxt.nex([text], min_confidence=0.3, include_types=True, include_categories=True, include_abstract=True, include_lod=True, include_alternate_labels=True)

			entities_dict = create_entitiy_dict(response)
		except:
			print(sys.exc_info()[0], "occurred.")
			return 0

		return entities_dict

	def create_entitiy_dict(response):
		entity_dict = {}

		for item in response['annotations']:
			if item['title'] not in list(entity_dict.keys()):
				entity_dict[item['title']] = []		
			entity_dict[item['title']].append([item])

		return entity_dict




	def create_mention_dataframe(text_df, datatxt):

		
		mentions_data = []

		for text_row in text_df.itertuples():
			
			count = 0

			text = text_row[4]

			mentions_dict = get_dande_entities_dict(text, datatxt)
			count +=1

			if mentions_dict == 0:
				print(text_row[0], " ... NOT AVAILABLE")

			else:
				text_id = text_row[0]
				father_id = text_row[1]
				father_title = text_row[2]
				author_name = text_row[3]
				print("Text ID", text_id, father_id, father_title, "Author Name", author_name)
				#father_location = text_row[6]
				source = "Dandelion"

				for keyy in mentions_dict.keys():
					obj_list = mentions_dict[keyy]
					for dic in obj_list:		
						start = dic[0]['start']
						end = dic[0]['end']
						mention = dic[0]['spot']
						confidence = dic[0]['confidence']
						entity_name = dic[0]['title']
						entity_description = dic[0]['abstract']
						entity_link = dic[0]['lod']['dbpedia']
						#entity_label = dic[0]['label']
						try:
							entity_categories = dic[0]['categories']
						except KeyError:
							entity_categories = [""]
							
						entity_types = dic[0]['types']

						mentions_data.append([text_id, father_id, father_title, author_name, source, 
						mention, start, end, entity_name, entity_link, confidence, entity_description,
						entity_categories, entity_types])

			print(text_row[0], " ... OK")

		column_names = ["Text_ID", "Father_ID", "Father_Name",  "Author_name", "Source", "Mention text", "Start_pos", "End_pos", "Entity Name",
						"DBpedia URL", "Confidence", "Description",
						"Semantic Categories", "DBpedia Types"]

		text_mentions_df = pd.DataFrame(mentions_data, columns=column_names)
		
		#text_mentions_df.to_pickle("Files/mentions_df_filtered_by_book.pkl")

		return text_mentions_df

	
	text_df_final = text_df
	#text_df_final.index = text_df.index
	#text_df_final.set_index('Text_ID',drop=False,inplace=True)

	datatxt = DataTXT(token="ADD-TOKEN-HERE")



	mentions_df_raw = create_mention_dataframe(text_df, datatxt)

	

	return mentions_df_raw, text_df_final


def filter_mentions_df_type(mentions_df_raw: pd.DataFrame) -> pd.DataFrame:

	print(len(mentions_df_raw), " Before")
	
	filter_rows = []
	for row in mentions_df_raw.itertuples():
		#print(row[14])
		types = row[14]
		#'http://dbpedia.org/ontology/Person', 
		types_filter = ['http://dbpedia.org/ontology/Band', 'http://dbpedia.org/ontology/TelevisionShow', 'http://dbpedia.org/ontology/VideoGame', 'http://dbpedia.org/ontology/MusicalWork', 'http://dbpedia.org/ontology/Film']
	
		add_row = True
		for type1 in types_filter:
			if type1 in types:
				add_row = False

		if add_row:
			filter_rows.append(row[0])


	mentions_df_raw = mentions_df_raw[mentions_df_raw.index.isin(filter_rows)]  
	print(len(mentions_df_raw), " After Types removed")


	filter_list = ["(band)", "song", "album", "American", "film", "(magazine)", "series", "Grand_Slam_", "(Language)"]

	for item in filter_list:
		mentions_df_raw =  mentions_df_raw[mentions_df_raw["DBpedia URL"].str.contains(item)==False]

	mentions_df_filtered_type = mentions_df_raw
	print(len(mentions_df_filtered_type), "After string matches removed")

	return mentions_df_filtered_type







def filter_mentions_df_confidence(mentions_df_filtered_type: pd.DataFrame, confidence:int=0.65) -> pd.DataFrame:

	mentions_df_filtered_confidence = mentions_df_filtered_type[mentions_df_filtered_type['Confidence']>confidence]
	print(len(mentions_df_filtered_confidence), " After Confidence filter")

	return mentions_df_filtered_confidence



def enhance_mentions_df(mentions_df_filtered_confidence: pd.DataFrame, text_df:pd.DataFrame) -> pd.DataFrame:

	def get_dbpedia_entities(text):

		doc = nlp(text)
		results_dbpedia = [(ent._.dbpedia_raw_result) for ent in doc.ents]

		return results_dbpedia


	print(len(mentions_df_filtered_confidence), " mentions before extension! Starting to enhance mentions...")

	concepts_info_df = mentions_df_filtered_confidence.groupby('DBpedia URL')[['Description','Semantic Categories', 'Entity Name', 'DBpedia Types']].agg('max')

	concepts_dict_w_occurences = {}
	for row in mentions_df_filtered_confidence.itertuples():
		#print(row[9], row[10])
		concept = row[10]
		if concept in concepts_dict_w_occurences.keys():
			concepts_dict_w_occurences[concept].append(row[1])
		else:
			concepts_dict_w_occurences[concept] = [row[1]]



	nlp = spacy.load('en_core_web_sm')

	nlp.add_pipe('dbpedia_spotlight', config={'confidence':0.40})

	
	entity_list = list(concepts_dict_w_occurences.keys())
	#print(entity_list)

	entity_data_list = []
	count=0

	for text_row in text_df.itertuples():
		#print(text_row)
		count+=1
		if count%10 == 0:
			print(count)

		text_id = text_row[0]
		text = text_row[4]


		entities = get_dbpedia_entities(text)

		#print(entities)

		for entity in entities:
			if entity != None:
				entity_link = entity['@URI']
				#print(entity_link)
				mention = entity['@surfaceForm']
				
				if entity_link in entity_list and len(mention) > 3 and mention.lower() not in ["when","good","goods","life","idea","success"]:
					#print("--\n"*5, entity_link)
					
					if text_id not in concepts_dict_w_occurences[entity_link]:
						#print(count, " ", entity_link) 
						

						start = int(entity["@offset"])
						end = start + len(mention)

						entity_name = concepts_info_df.loc[entity_link,"Entity Name"]
						
						entity_description = concepts_info_df.loc[entity_link,"Description"]
						#entity_link = dbpedia_link
						entity_categories = concepts_info_df.loc[entity_link,"Semantic Categories"]
						entity_types = concepts_info_df.loc[entity_link,"DBpedia Types"]

						### POTENCIAL PROBLEMA ↓↓↓↓↓↓↓↓ Start e End Positions

						#start = len(text.title().split(concept_name)[0])
						#end = start + len(concept_name)

						### POTENCIAL PROBLEMA

						highlight_id = text_row[0]
						book_id = text_row[1]
						book_title = text_row[2]
						author_name = text_row[3]
						#book_location = text_row[6]
						source = "Expansion"
						#mention = concept_name

						confidence = 0.99
						
						entity_data_list.append([highlight_id, book_id, book_title, author_name, source, 
							mention, start, end, entity_name, entity_link, confidence, entity_description,
							entity_categories, entity_types])


	column_names = ["Text_ID", "Father_ID", "Father_Name", "Author_name", "Source", "Mention text", "Start_pos", "End_pos", "Entity Name",
						"DBpedia URL", "Confidence", "Description",
						"Semantic Categories", "DBpedia Types"]

	extension_mentions_df = pd.DataFrame(entity_data_list, columns=column_names)

	print(len(extension_mentions_df), " additional mentions identified")


	mentions_df_extended = pd.concat([mentions_df_filtered_confidence, extension_mentions_df], axis=0)

	print(len(mentions_df_extended), " mentions in Total")
	return mentions_df_extended




def filter_mentions_df_multiple_occ(mentions_df_extended: pd.DataFrame) -> pd.DataFrame:


	multiple_occurences_tracker = mentions_df_extended.groupby("DBpedia URL")[['Text_ID','Father_ID']].agg('nunique')

	keep_concept = []

	for row in multiple_occurences_tracker.itertuples():

		if row[1] > 1:

			keep_concept.append(row[0])
			#drop_concept.append(row[0])

	mentions_df_filtered_multiple_occurrences = mentions_df_extended.loc[mentions_df_extended['DBpedia URL'].isin(keep_concept)]
	print(len(mentions_df_filtered_multiple_occurrences), " After Multiple Occurences filter")

	return mentions_df_filtered_multiple_occurrences



def filter_mentions_df_conceptnet(mentions_df_filtered_multiple_occurrences: pd.DataFrame, dbpedia_to_conceptnet_prev:dict, conceptnet_to_dbpedia_prev:dict):

	
	concepts_list = list(mentions_df_filtered_multiple_occurrences['DBpedia URL'].unique())
	print("Startinf concepts filter for ConceptNet")
	#print("Number of Concepts: ", len(concepts_list), concepts_list)

	relation = "/r/ExternalURL"

	DBpedia_to_ConceptNet_dict = dbpedia_to_conceptnet_prev
	ConceptNet_to_DBpedia_dict = conceptnet_to_dbpedia_prev

	dbpedia_url_keys = dbpedia_to_conceptnet_prev.keys()

	not_found_list = []

# GRANDE FOR

	for concept_url in concepts_list:

		if concept_url not in dbpedia_url_keys:

		#print(concept_url)

			found = False

			query_url = "http://api.conceptnet.io/query?end=" + concept_url + "&rel=" + relation  + "&limit=100"
			response = requests.get(query_url)
			obj = response.json()

			conceptNet_name = [edge['start']['@id'] for edge in obj['edges'] if edge['start']['language']=="en"]

			#print(conceptNet_name)
			if conceptNet_name != []:

				DBpedia_to_ConceptNet_dict[concept_url] = conceptNet_name[0]
				ConceptNet_to_DBpedia_dict[conceptNet_name[0]] = concept_url

				print(conceptNet_name[0], " was BEAUTIFULLY found in ConceptNet.")

			else:
				dbpedia_name = concept_url.split("/resource/")[1].replace("-", "_")

				candidate_name = "/c/en/" + dbpedia_name.split("_(")[0].lower()
				test = requests.get('http://api.conceptnet.io'+ candidate_name).json()
				
				if "_(" in dbpedia_name:

					candidate_name_specific = "/c/en/"+ dbpedia_name.split("_(")[0].lower() + "/n/wp/" + dbpedia_name.split("_(")[1].split(")")[0].lower()
					test_specific = requests.get('http://api.conceptnet.io'+ candidate_name_specific).json()
				

					if test_specific['edges'] != []:

						print(candidate_name_specific, " was Found with specificity, and has NO direct link to DBpedia")

						DBpedia_to_ConceptNet_dict[concept_url] = candidate_name_specific
						ConceptNet_to_DBpedia_dict[candidate_name_specific] = concept_url
						found = True
					else:
						print(candidate_name_specific, " WAS NOT FOUND with specificity, trying again with only the concept...")



				if test['edges'] != [] and found == False:

					print(candidate_name, " was Found, and has NO direct link to DBpedia.")

					DBpedia_to_ConceptNet_dict[concept_url] = candidate_name
					ConceptNet_to_DBpedia_dict[candidate_name] = concept_url

				else:
					if found == False:
						print(candidate_name, " WAS NOT FOUND at all.")
						not_found_list.append(concept_url)
						DBpedia_to_ConceptNet_dict[concept_url] = ""
						#ConceptNet_to_DBpedia_dict[candidate_name] = concept_url

			


	drop_mentions_df = mentions_df_filtered_multiple_occurrences

	print("Number of Concepts: ", len(concepts_list), concepts_list)
	print(not_found_list, "-----")
	for concept_url in not_found_list:
		if concept_url != "http://dbpedia.org/resource/Personal_knowledge_management":
			print(concept_url)
			print(len(drop_mentions_df["DBpedia URL"].unique()))
			match_string = concept_url.split("_(")[0]
			drop_mentions_df =  drop_mentions_df[drop_mentions_df["DBpedia URL"].str.contains(match_string)==False]


	mentions_df_filtered_conceptnet = drop_mentions_df

	print(len(mentions_df_filtered_conceptnet), " After ConceptNet filter")


	# ConceptNet_to_DBpedia_dict not returned (unused)

	dbpedia_to_conceptnet = DBpedia_to_ConceptNet_dict

	conceptnet_to_dbpedia = ConceptNet_to_DBpedia_dict

	return mentions_df_filtered_conceptnet, dbpedia_to_conceptnet, conceptnet_to_dbpedia




def generate_files_mentions_df_concept_list(mentions_df_filtered_conceptnet: pd.DataFrame) -> list:

	concepts_list = list(mentions_df_filtered_conceptnet['DBpedia URL'].unique())

	print("Number of Concepts: ", len(concepts_list))

	concepts_list_final = concepts_list

	mentions_df_final = mentions_df_filtered_conceptnet.copy()

	return mentions_df_final, concepts_list, concepts_list_final


