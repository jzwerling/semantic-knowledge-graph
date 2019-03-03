find_edge = lambda node_one, node_two, field_name: {
	"query" : {
		"bool": {
						"must": [
							{
								"match_phrase": {
											field_name : node_one
										}
								},
								{
										"match_phrase": {
												field_name : node_two
										}
								}
						]
				}
		},
	"aggregations": {
		"keywords" : {
			"significant_text" : { 
				"field" : field_name, "min_doc_count":2, "gnd":{}
			}
		}
	}
 }

index_settings = lambda doc_type : {
	"settings": {
		"index": {
			"analysis": {
				"tokenizer": {
					"comma": {
						"type": "pattern",
						"pattern": ","
					}
				},
				"analyzer": {
					"entity_analyzer": {
						"type": "custom",
						"tokenizer": "comma",
						"filter": ["trim","lowercase"]
					}
				}
			}
		}
	},
	"mappings": {
		doc_type: {
		"properties": {
			"entities": {
				"type": "text",
				"analyzer": "entity_analyzer"
			},
			"body_text" : {
				"type" : "text",
				"fields" : {
					"keyword" : {
						"type" : "keyword"
					}
				}
			},
			"tags" : {
				"type" : "text",
				"fields" : {
					"keyword" : {
						"type" : "keyword"
					}
				}
			}
		}
	}}
}