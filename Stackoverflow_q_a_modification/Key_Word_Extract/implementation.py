# coding=utf-8
import finalTest

text = u"""Dulanjana is a Senior Software Engineer at WSO2.

Prior to joining WSO2, Yasara worked at Millennium Information Technologies as a Software Engineer where he was part 
of the post trade team that developed clearing, settlement, risk and CSD solutions for Exchange Systems. He holds a 
BSc. Engineering (Hons) in Electronic & Telecommunication Engineering from the Faculty of Engineering, University Of 
Moratuwa and currently he works in NASA Institute, USA.

He enjoys photography and watching cricket during his leisure time."""

rake = finalTest.KeyWordExtract()
rake.extract(text)

# If most of the words have the same score how to choose the best out of the score.
#



# Stop the server. Try to remove the folder content in [WSO2_HOME]\repository\deployment\server\servicemetafiles\ and
#  start the server. Make a copy of this file in another location before that. I was able to solve my problem. The
# WSO2 have two tutorials, to each folder. One, from carbon.bat and integrator.bat,
# is the 'docs.wso2.com/display/EI600/Installing+as+a+Windows+Service'. Another is:
# 'docs.wso2.com/display/Carbon420/Installing+as+a+Windows+Service'. With serve for wso2server.bat. Thank you everyone.
