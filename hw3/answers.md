# HW3 - Proabilistic ContextFree Grammar

### Task 1
Arthur is the king .
`P(Arthur|Proper)=1/8`
`P(is|VerbT)=1/6`
P(the|Det)=1/9
P(king|Noun)=1/21
P(.|Misc)=1/183
$$ x = {-b \pm \sqrt{b^2-4ac} \over 2a}. $$
Parsing

=1*1/6*(1/7)^5
![](http://latex.codecogs.com/gif.latex?\\P(S2|ROOT)P(+Proper|S2)P(Proper +VerbT|+Proper)P(VerbT +Det|+VerbT)P(Det +Noun|+Det)P(Noun +Misc|+Noun)P(Misc|+Misc))
Therefore, this PCFG implements a bigram language model. 

### Task 2
The main difference is that the PCFG that only contains grammar 1 cannot parse most of the sentences. This is because grammar 1 does not have rules such as S1 -> +Misc to parse sentences that begin with a *Misc* word.
