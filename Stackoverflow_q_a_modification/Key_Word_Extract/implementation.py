# coding=utf-8
import finalTest

text = u"""I often apply natural language processing for purposes of automatically extracting structured information 
from unstructured (text) datasets. One such task is the extraction of important topical words and phrases from 
documents, commonly known as terminology extraction or automatic keyphrase extraction. Keyphrases provide a concise 
description of a document’s content; they are useful for document categorization, clustering, indexing, search, 
and summarization; quantifying semantic similarity with other documents; as well as conceptualizing particular 
knowledge domains. Despite wide applicability and much research, keyphrase extraction suffers from poor performance 
relative to many other core NLP tasks, partly because there’s no objectively “correct” set of keyphrases for a given 
document. While human-labeled keyphrases are generally considered to be the gold standard, humans disagree about what 
that standard is! As a general rule of thumb, keyphrases should be relevant to one or more of a document’s major 
topics, and the set of keyphrases describing a document should provide good coverage of all major topics. (They 
should also be understandable and grammatical, of course.) The fundamental difficulty lies in determining which 
keyphrases are the most relevant and provide the best coverage. As described in Automatic Keyphrase Extraction: A 
Survey of the State of the Art, several factors contribute to this difficulty, including document length, structural 
inconsistency, changes in topic, and (a lack of) correlations between topics. """

rake = finalTest.KeyWordExtract()
rake.extract(text)

# If most of the words have the same score how to choose the best out of the score.
#



# Stop the server. Try to remove the folder content in [WSO2_HOME]\repository\deployment\server\servicemetafiles\ and
#  start the server. Make a copy of this file in another location before that. I was able to solve my problem. The
# WSO2 have two tutorials, to each folder. One, from carbon.bat and integrator.bat,
# is the 'docs.wso2.com/display/EI600/Installing+as+a+Windows+Service'. Another is:
# 'docs.wso2.com/display/Carbon420/Installing+as+a+Windows+Service'. With serve for wso2server.bat. Thank you everyone.
