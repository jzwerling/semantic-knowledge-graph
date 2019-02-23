from xml.dom import minidom
from elasticsearch import Elasticsearch
import re


es = Elasticsearch()
pattern = re.compile('(<[^>]*>)|(\\"|\\n|\\r)')


def populate_index(source_file, index_name, doc_type, field_mapping):	
	items = source_file.getElementsByTagName('row')
	for item in items:
		item_dict = {}
		for k, v in field_mapping.items():
			item_dict[v] = pattern.sub('', item.getAttribute(k))
		if len(item_dict['body_text']) > 0: 
			result = es.index(index=index_name, doc_type=doc_type, id=item_dict['id'], body=item_dict)

	es.indices.refresh(index=index_name)

#https://archive.org/download/stackexchange
parsed_doc = minidom.parse("Comments.xml")
populate_index(parsed_doc, "scifi_comments", "comments", {'Id':'id', 'Text': 'body_text', 'PostId':'post_id'})
parsed_doc = minidom.parse("Posts.xml")
populate_index(parsed_doc, "scifi_posts", "posts", {'Id':'id', 'Body': 'body_text', 'Tags':'tags'})