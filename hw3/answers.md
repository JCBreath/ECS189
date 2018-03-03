# HW3 - Proabilistic ContextFree Grammar

### Task 1
For example, for sentence `Arthur is the king .` we have `P(T, S)=1*1/6*(1/7)^5*(1/8)*(1/6)*(1/9)*(1/21)*(1/183)`  
Sentence:
```
P(Arthur|Proper)P(is|VerbT)P(the|Det)P(king|Noun)P(.|Misc) 
= (1/8)*(1/6)*(1/9)*(1/21)*(1/183)
```
Parse:
```
P(S2|ROOT)P(+Proper|S2)P(Proper +VerbT|+Proper)P(VerbT +Det|+VerbT)P(Det +Noun|+Det)P(Noun +Misc|+Noun)P(Misc|+Misc)
= 1*1/6*(1/7)^5
```

Therefore, this PCFG implements a bigram language model. 

### Task 2
The main difference is that the PCFG that only contains grammar 1 cannot parse most of the sentences. This is because grammar 1 does not have rules such as S1 -> +Misc to parse sentences that begin with a *Misc* word.
