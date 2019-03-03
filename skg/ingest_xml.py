from xml.dom import minidom
from elasticsearch import Elasticsearch
import es_queries
import re
import spacy
import en_core_web_sm


es = Elasticsearch()
pattern = re.compile('(<[^>]*>)|(\\"|\\n|\\r)')
nlp = en_core_web_sm.load()


def populate_index(source_file, index_name, doc_type, field_mapping, index_entities=False):	
	es.indices.create(index_name, es_queries.index_settings(doc_type))
	
	items = source_file.getElementsByTagName('row')
	for item in items:
		item_dict = {}
		for k, v in field_mapping.items():
			item_dict[v] = pattern.sub('', item.getAttribute(k))

		if index_entities:
			item_dict['entities'] = get_entities(item_dict['body_text'])

		if len(item_dict['body_text']) > 0: 
			result = es.index(index=index_name, doc_type=doc_type, id=item.getAttribute('Id'), body=item_dict)

	es.indices.refresh(index=index_name)

def get_entities(body_text):
	doc = nlp(body_text)
	return 	",".join([(e.text) for e in doc.ents])

parsed_doc = minidom.parse("Comments.xml")
populate_index(parsed_doc, "scifi_comments", "comments", {'Text': 'body_text', 'PostId':'post_id'}, True)
#parsed_doc = minidom.parse("Posts.xml")
#populate_index(parsed_doc, "scifi_posts", "posts", {'Body': 'body_text', 'Tags':'tags'}, True)
