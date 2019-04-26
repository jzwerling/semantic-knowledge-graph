from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import es_queries


es = Elasticsearch()


def get_edge_for_two_nodes(nodes, search_field, indexes_to_search, depth=1, level=1):
    query_body = es_queries.find_edge(nodes[0], nodes[1], search_field)

    result = es.search(index=indexes_to_search, body=query_body)
    buckets = result['aggregations']['keywords']['buckets']

    
    print("level: {} nodes: {} | {}".format(level, nodes[0], nodes[1]))
    for b in buckets:
        if not b['key'] in nodes:
            print("term: {} | docs: {} | bg_ount: {} | score: {}%".format(b['key'], b['doc_count'], 
                b['bg_count'], int(b['score']*100)))
            if depth > 1:
                for n in nodes:
                    get_edge_for_two_nodes([n, b['key']], search_field, indexes_to_search, depth-1, level+1)

                    
get_edge_for_two_nodes(["jean grey", "in love"], "body_text", ["scifi_posts", "scifi_comments"])
#get_edge_for_two_nodes(["vader", "the force"], "body_text", ["scifi_posts", "scifi_comments"], 3)
#get_edge_for_two_nodes(["marty mcfly", "time travel"], "body_text", ["scifi_posts", "scifi_comments"], 5)

get_edge_for_two_nodes(["bruce banner", "iron man"], "entities", ["scifi_posts", "scifi_comments"], 2)
#get_edge_for_two_nodes(["darth vader", "luke skywalker"], "entities", ["scifi_posts"], 3)
