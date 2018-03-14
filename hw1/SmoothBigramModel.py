import math, collections

class SmoothBigramModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    # Tip: To get words from the corpus, try
    #    for sentence in corpus.corpus:
    #       for datum in sentence.data:  
    #         word = datum.word
    for sentence in corpus.corpus:
        for i in xrange(1,len(sentence.data) - 1):
            curr = sentence.data[i].word
            prev = sentence.data[i-1].word
            self.bigramCounts[(prev, curr)] = self.bigramCounts[(prev, curr)] + 1
            self.unigramCounts[prev] = self.unigramCounts[prev] + 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0 
    for i in xrange(1,len(sentence) - 1):
      prev = sentence[i-1]
      curr = sentence[i]
      count = self.bigramCounts[(prev, curr)] + 1
      score += math.log(count)
      score -= math.log(len(self.unigramCounts))
    return score
