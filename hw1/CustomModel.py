import math, collections

class CustomModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.trigramCounts = collections.defaultdict(lambda: 0)
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
        if i > 1:
          prev = sentence.data[i-1].word
          self.bigramCounts[(prev, curr)] = self.bigramCounts[(prev, curr)] + 1 # get bigram counts
        if i > 2:
          prev = sentence.data[i-1].word
          prev_2 = sentence.data[i-2].word
          self.trigramCounts[(prev_2, prev, curr)] = self.trigramCounts[(prev_2, prev, curr)] + 1 # get trigram counts
        self.unigramCounts[curr] = self.unigramCounts[curr] + 1 # get unigram counts
        self.total += 1 # get N

    
      

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0.0

    for i in xrange(3,len(sentence) - 1):
      prev_2 = sentence[i-2]
      prev = sentence[i-1]
      curr = sentence[i]
      # trigram count
      tri_count = self.trigramCounts[(sentence[i-2], prev, curr)]
      # bigram count
      bi_count = self.bigramCounts[(prev_2, prev)]
      # unigram count
      uni_count = self.unigramCounts[prev]
      
      # use basic trigram model
      if tri_count > 0:
        score += math.log(tri_count)
        score -= math.log(bi_count)
        continue
      else:
        bi_count = self.bigramCounts[(prev, curr)]
      
      # use basic bigram model
      if bi_count > 0:
        score += math.log(bi_count)
        score -= math.log(uni_count)
        continue
      else:
        uni_count = self.unigramCounts[curr] + 1 # add one smoothing

      # use smoothed unigram model
      score += math.log(uni_count) # alpha = 0.4
      score -= math.log(self.total + len(self.unigramCounts)) # N + V

    return score
