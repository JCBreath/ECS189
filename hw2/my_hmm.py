import sys,re
from itertools import izip
from collections import defaultdict

TAG_FILE=sys.argv[1]
TOKEN_FILE=sys.argv[2]

vocab={}
OOV_WORD="OOV"
INIT_STATE="init"
FINAL_STATE="final"

emissions={}
tri_transitions={}
bi_transitions={}
transitionsTotal=defaultdict(int)
emissionsTotal=defaultdict(int)

with open(TAG_FILE) as tagFile, open(TOKEN_FILE) as tokenFile:
	for tagString, tokenString in izip(tagFile, tokenFile):

		tags=re.split("\s+", tagString.rstrip())
		tokens=re.split("\s+", tokenString.rstrip())
		pairs=zip(tags, tokens)

		prev_2 = INIT_STATE
		prev = INIT_STATE

		t = 1

		for (tag, token) in pairs:
			
			
			
			if token not in vocab:
				vocab[token]=1
				token=OOV_WORD


			if (prev_2, prev, tag) not in tri_transitions:
				tri_transitions[(prev_2, prev, tag)]=0

			tri_transitions[(prev_2, prev, tag)]+=1
			prev_2 = prev


			if (tag, token) not in emissions:
				emissions[(tag, token)]=0

			if(prev, tag) not in bi_transitions:
				bi_transitions[(prev,tag)]=0

			emissions[(tag, token)]+=1
			emissionsTotal[tag]+=1

			bi_transitions[(prev,tag)]+=1
			transitionsTotal[prev]+=1

			prev = tag


		if (prev_2, prev, FINAL_STATE) not in tri_transitions:
			tri_transitions[(prev_2,prev,FINAL_STATE)]=0

		tri_transitions[(prev_2,prev,FINAL_STATE)]+=1

		if (prev,FINAL_STATE) not in bi_transitions:
			bi_transitions[(prev,FINAL_STATE)]=0

		bi_transitions[(prev,FINAL_STATE)]+=1
		transitionsTotal[prev]+=1


for (prev, tag) in bi_transitions:
	print "bi_trans %s %s %s" % (prev, tag, float(bi_transitions[(prev, tag)]) / transitionsTotal[prev])


for (prev_2, prev, tag) in tri_transitions:
	print "trans %s %s %s %s" % (prev_2, prev, tag, float(tri_transitions[(prev_2, prev, tag)]) / bi_transitions[(prev, tag)])

for (tag,token) in emissions:
	print "emit %s %s %s " % (tag, token, float(emissions[(tag,token)]) / emissionsTotal[tag])




