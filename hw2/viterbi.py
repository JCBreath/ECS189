# Siyuan Yao

import math, fileinput, sys, re
import numpy

HMM_FILE=sys.argv[1]

OOV_WORD="OOV"
INIT_STATE="init"
FINAL_STATE="final"

vocab={}
transition={}
bi_transition={}
emission={}
# viterbi scores
V={}
# viterbi backpointers
bps={}
# viterbi states
states={}

# Load HMM and store probabilities in log()
with open(HMM_FILE) as hmmFile:
	for line in hmmFile:
		# transition
		if line[0] == 't':
			line = line.rstrip()
			regex = r"(\S*)\s(\S*)\s(\S*)\s(\S*)\s(\S*)"
			match = re.search(regex, line)
			transition[(match.group(2),match.group(3),match.group(4))] = math.log(float(match.group(5)))
			states[match.group(2)] = 1
			states[match.group(3)] = 1
			states[match.group(4)] = 1

		# bi_transition
		if line[0] == 'b':
			line = line.rstrip()
			regex = r"(\S*)\s(\S*)\s(\S*)\s(\S*)"
			match = re.search(regex, line)
			bi_transition[(match.group(2),match.group(3))] = math.log(float(match.group(4)))
			states[match.group(2)] = 1
			states[match.group(3)] = 1

		# emission
		if line[0] == 'e':
			line = line.rstrip()
			regex = r"(\S*)\s(\S*)\s(\S*)\s(\S*)"
			match = re.search(regex, line)
			emission[(match.group(2),match.group(3))] = math.log(float(match.group(4)))
			states[match.group(2)] = 1
			vocab[match.group(3)] = 1




for line in sys.stdin:
	V = {}
	bps = {}





	sentence = line.split()
	sentence[0] = sentence[0][:1].lower() + sentence[0][1:]
	



	for i in xrange(0,len(sentence)):
		word = sentence[i]
		if word not in vocab:
			sentence[i] = OOV_WORD
	

	V[(-1,INIT_STATE,INIT_STATE)] = 0.0

	'''
	for q in states:
		if(q,sentence[0]) in emission:
			
			bps[(0,INIT_STATE,q)] = (INIT_STATE,INIT_STATE)
	'''

	#prev = sentence[0]
	#prev_2 = INIT_STATE
	#t = 1

	for i in xrange(0,len(sentence)):
		word = sentence[i]

		tri_found = 0

		for q in states:
			if(q, word) in emission:

				for qq in states:

					for qqq in states:
						
						if (qqq, qq, q) in transition: 			
							
							tri_found = 1
							if (i-1,qqq,qq) in V:

								v = V[(i-1,qqq,qq)] + transition[(qqq,qq,q)] + bi_transition[(qq,q)] + emission[(q,word)]
								
								if (i,qq,q) not in V or v > V[(i,qq,q)]:
									V[(i,qq,q)] = v
									bps[(i,qq,q)] = (qqq, qq)
						


						
						else:
							if (qq, q) in bi_transition:
								if (i-1,qqq,qq) in V:

									v = V[(i-1,qqq,qq)] + bi_transition[(qq,q)] + emission[(q,word)] - 100
								
									if (i,qq,q) not in V:
										V[(i,qq,q)] = v
										bps[(i,qq,q)] = (qqq, qq)
							else:
								if (i-1,qqq,qq) in V:

									v = V[(i-1,qqq,qq)] + emission[(q,word)] - 100000
									#print v
									if (i,qq,q) not in V:
										V[(i,qq,q)] = v
										bps[(i,qq,q)] = (qqq, qq)
						
			
									
	

	q = FINAL_STATE
	i = len(sentence)

	for qq in states:
		for qqq in states:
			if (qqq, qq, q) in transition:
				if(i - 1,qqq,qq) in V:

					v = V[(i - 1,qqq,qq)] + transition[(qqq,qq,q)]
					
					if(i,qq,q) not in V or v > V[(i,qq,q)]:
						V[(i,qq,q)] = v
						bps[(i,qq,q)] = (qqq, qq)


	tags={}

	for qq in states:
		if(i,qq,FINAL_STATE) in bps:
			tags[i-1] = bps[(i,qq,FINAL_STATE)][1]
			tags[i-2] = bps[(i,qq,FINAL_STATE)][0]

	#print i - 2

	#print bps

	for i in xrange(3, len(sentence) + 1):
		j = len(sentence) - i
		#print j
		#print (j,bps[(j+2,tags[j+1],tags[j+2])])
		tags[j] = bps[(j+2,tags[j+1],tags[j+2])][0]

	output = []

	#print tags

	for i in tags:
		if tags[i] != INIT_STATE:
			output.append(tags[i])
	print (' '.join(output))

	'''
	sen = []
	for i in bps:
		if bps[i] != INIT_STATE:
			sen.append(bps[i])
	print (' '.join(sen))
	'''
	#print(''.join(str(e) for e in bps))
		#prev_2 = prev
		#prev = curr

	
	