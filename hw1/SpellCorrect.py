##
# Credit Zhou Yu, Dan Jurafsky, Peter Norvig
# Updated Kevin Jesse
# Open source code under MIT license
##

import math
from Datum import Datum
from Sentence import Sentence
from Corpus import Corpus
from UniformModel import UniformModel
from UnigramModel import UnigramModel
from BackoffModel import BackoffModel
from SmoothUnigramModel import SmoothUnigramModel
from SmoothBigramModel import SmoothBigramModel
from CustomModel import CustomModel
from EditModel import EditModel
from SpellingResult import SpellingResult
import types
import re, collections

class SpellCorrect:
  """Spelling corrector for sentences. Holds edit model, language model and the corpus."""

  def __init__(self, lm, corpus):
    self.languageModel = lm
    self.editModel = EditModel('data/count_1edit.txt', corpus)

  def correctSentence(self, sentence):
    """Assuming exactly one error per sentence, returns the most probable corrected sentence.
       Sentence is a list of words."""

    if len(sentence) == 0:
      return []

    bestSentence = sentence[:] #copy of sentence
    bestScore = float('-inf')
    
    for i in xrange(1, len(sentence) - 1): #ignore <s> and </s>
      
      best_edit = sentence[:] # initialize best edit at i
      
      edits = self.editModel.editProbabilities(sentence[i]) # get edits and log-probabilities

      score = float('-inf') # initialize score for edit

      # start test edits
      for j in xrange(0, len(edits)):
        edited_s = sentence[:] # initialize a sentence to be edited
        edited_s[i] = edits[j][0] # make edit
        em_prob = edits[j][1] # get this edit probability
        s_prob = self.languageModel.score(edited_s) # get language model score
        score = max(score, em_prob + s_prob) # update max edit score
        if score == em_prob + s_prob:
          best_edit = edited_s[:] # update best edit

      bestScore = max(score, bestScore) # update max sentence score
      
      if bestScore == score:
        bestSentence = best_edit # update best sentence

    return bestSentence

  def evaluate(self, corpus):  
    """Tests this speller on a corpus, returns a SpellingResult"""
    numCorrect = 0
    numTotal = 0
    testData = corpus.generateTestCases()
    for sentence in testData:
      if sentence.isEmpty():
        continue
      errorSentence = sentence.getErrorSentence()
      hypothesis = self.correctSentence(errorSentence)
      if sentence.isCorrection(hypothesis):
        numCorrect += 1
      numTotal += 1
    return SpellingResult(numCorrect, numTotal)

  def correctCorpus(self, corpus): 
    """Corrects a whole corpus, returns a JSON representation of the output."""
    string_list = [] # we will join these with commas,  bookended with []
    sentences = corpus.corpus
    for sentence in sentences:
      uncorrected = sentence.getErrorSentence()
      corrected = self.correctSentence(uncorrected)
      word_list = '["%s"]' % '","'.join(corrected)
      string_list.append(word_list)
    output = '[%s]' % ','.join(string_list)
    return output

def main():
  """Trains all of the language models and tests them on the dev data. Change devPath if you
     wish to do things like test on the training data."""

  trainPath = 'data/tagged-train.dat'
  trainingCorpus = Corpus(trainPath)

  devPath = 'data/tagged-dev.dat'
  devCorpus = Corpus(devPath)
  
  print 'Unigram Language Model: ' 
  unigramLM = UnigramModel(trainingCorpus)
  unigramSpell = SpellCorrect(unigramLM, trainingCorpus)
  unigramOutcome = unigramSpell.evaluate(devCorpus)
  print str(unigramOutcome)

  print 'Uniform Language Model: '
  uniformLM = UniformModel(trainingCorpus)
  uniformSpell = SpellCorrect(uniformLM, trainingCorpus)
  uniformOutcome = uniformSpell.evaluate(devCorpus) 
  print str(uniformOutcome)

  print 'Smooth Unigram Language Model: ' 
  smoothUnigramLM = SmoothUnigramModel(trainingCorpus)
  smoothUnigramSpell = SpellCorrect(smoothUnigramLM, trainingCorpus)
  smoothUnigramOutcome = smoothUnigramSpell.evaluate(devCorpus)
  print str(smoothUnigramOutcome)

  print 'Smooth Bigram Language Model: '
  smoothBigramLM = SmoothBigramModel(trainingCorpus)
  smoothBigramSpell = SpellCorrect(smoothBigramLM, trainingCorpus)
  smoothBigramOutcome = smoothBigramSpell.evaluate(devCorpus)
  print str(smoothBigramOutcome)
  
  print 'Backoff Language Model: '
  backoffLM = BackoffModel(trainingCorpus)
  backoffSpell = SpellCorrect(backoffLM, trainingCorpus)
  backoffOutcome = backoffSpell.evaluate(devCorpus)
  print str(backoffOutcome)
  
  print 'Custom Language Model: '
  customLM = CustomModel(trainingCorpus)
  customSpell = SpellCorrect(customLM, trainingCorpus)
  customOutcome = customSpell.evaluate(devCorpus)
  print str(customOutcome)

if __name__ == "__main__":
    main()
