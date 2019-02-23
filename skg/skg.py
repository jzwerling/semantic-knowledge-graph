from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import es_queries


es = Elasticsearch()


def get_edge_for_two_nodes(nodes, search_field, indexes_to_search, levels=2):
    node_terms = nodes[0].split() + nodes[1].split()
    query_body = es_queries.find_edge(nodes[0], nodes[1], search_field)

    result = es.search(index=indexes_to_search, body=query_body)

    doc_count = result['aggregations']['keywords']['doc_count']
    print("doc count is: {}".format(doc_count))
    buckets = result['aggregations']['keywords']['buckets']

    
    print("nodes: {} | {}".format(nodes[0], nodes[1]))
    for b in buckets:
        #remove terms that are in the node phrases
        if not b['key'] in node_terms:
            print("term: {} | docs: {} | bg_ount: {} | score: {}%".format(b['key'], b['doc_count'], b['bg_count'], int(b['score']*100)))
            if levels > 2:
                for n in nodes:
                    get_edge_for_two_nodes([n, b['key']], "body_text", ["scifi_posts", "scifi_comments"], levels-1)

get_edge_for_two_nodes(["jean grey", "in"], "body_text", ["scifi_posts", "scifi_comments"])
#get_edge_for_two_nodes(["vader", "the force"], "body_text", ["scifi_posts", "scifi_comments"], 3)
#get_edge_for_two_nodes(["marty mcfly", "time travel"], "body_text", ["scifi_posts", "scifi_comments"], 5)