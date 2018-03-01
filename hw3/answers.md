# HW3 - Proabilistic ContextFree Grammar

### Task 1
This PCFG has two parameters: grammar that works as bigram transition probabilities, and lexicon that works as emission probabilities. 
After finding all valid parsing trees, it compares the probability (score) of each parsing tree, and selects the most probable one as the result. 
It is the same as using a forward algorithm to find hidden states of the last latent variable at the end of the sequence and the viterbi algorithm to find the most likely state sequence.
Therefore, this PCFG implements a bigram hidden Markov model. 

### Task 2
The main difference is that the PCFG that only contains grammar 1 cannot parse most of the sentences. This is because grammar 1 does not have rules such as S1 -> +Misc to parse sentences that begin with a *Misc* word.
