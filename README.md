# SemanticKnowledgeGraph
Implementation of Semantic Knowledge graph with Elasticsearch 6.6 and Python 3.7

Based on Trey Grainger's presentation here:
https://www.youtube.com/watch?v=JvuQX92zyi0&t=2124s
and white paper here:
https://arxiv.org/pdf/1609.00464.pdf

To recreate the Jean Grey example from the presentation, downloaded scifi.stackexchange.com.7z from https://archive.org/download/stackexchange, ingest_xml.py is used to populate the Elasticsearch indexes with the archive data.  As written, the code is looking for Posts.xml and Comments.xml in the same directory as ingest_xml.

skg.py takes the provided nodes and displays the terms that show how the nodes are related, effectively describing the edge that connects the nodes.  This is done through a query to es with two match_phrase conditions, one for each node supplied, results come from significant terms aggregation.  There is also an optional 'levels' parameter to indicate recursion depth.  If this is supplied, skg will iterate through the returned significant terms, and sequentially pair these with the orignal nodes to find more related terms.