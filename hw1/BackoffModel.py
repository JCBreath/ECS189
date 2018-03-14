import math, collections

class BackoffModel:

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
      for i in xrange(0,len(sentence.data)):
        curr = sentence.data[i].word
        if i > 0:
          prev = sentence.data[i-1].word
          self.bigramCounts[(prev, curr)] = self.bigramCounts[(prev, curr)] + 1 # get bigram counts
        self.unigramCounts[curr] = self.unigramCounts[curr] + 1 # get unigram counts
        self.total += 1 # get N

    
      

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0
    for i in xrange(1,len(sentence)):
      prev = sentence[i-1]
      curr = sentence[i]
      # bigram count
      bi_count = self.bigramCounts[(prev, curr)]
      # unigram count
      uni_count = self.unigramCounts[prev]

      # use basic bigram model
      if bi_count > 0:
        score += math.log(bi_count) # C(w_i|w_i-1)
        score -= math.log(uni_count) # C(w_i-1)
      # use smoothed unigram model
      else:
        uni_count = self.unigramCounts[curr] + 1 # add one smoothing
        score += math.log(0.4*uni_count) # alpha = 0.4
        score -= math.log(self.total + len(self.unigramCounts)) # N + V

    return score
