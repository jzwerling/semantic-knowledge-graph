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