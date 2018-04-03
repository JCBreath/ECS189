import sys
import getopt
import os
import math
import operator

from collections import defaultdict

class NaiveBayes:
    class TrainSplit:
        """
        Set of training and testing data
        """
        def __init__(self):
            self.train = []
            self.test = []

    class Document:
        """
        This class represents a document with a label. classifier is 'pos' or 'neg' while words is a list of strings.
        """
        def __init__(self):
            self.classifier = ''
            self.words = []

    def __init__(self):
        """
        Initialization of naive bayes
        """
        self.stopList = set(self.readFile('data/english.stop'))
        self.bestModel = False
        self.stopWordsFilter = False
        self.naiveBayesBool = False
        self.numFolds = 10 # should be 10

        # TODO
        # Implement a multinomial naive bayes classifier and a naive bayes classifier with boolean features. The flag
        # naiveBayesBool is used to signal to your methods that boolean naive bayes should be used instead of the usual
        # algorithm that is driven on feature counts. Remember the boolean naive bayes relies on the presence and
        # absence of features instead of feature counts.

        # When the best model flag is true, use your new features and or heuristics that are best performing on the
        # training and test set.

        # If any one of the flags filter stop words, boolean naive bayes and best model flags are high, the other two
        # should be off. If you want to include stop word removal or binarization in your best performing model, you
        # will need to write the code accordingly.
        
        self.pos_words = defaultdict(int)
        self.pos_total = 0 # sum_w in V(count(w,c))

        self.neg_words = defaultdict(int)
        self.neg_total = 0

        self.pos_rev = 0
        self.neg_rev = 0

        self.top_filter = 0
        self.top_filter_neg = 0

    def classify(self, words):
        """
        Classify a list of words and return a positive or negative sentiment
        """
        if self.stopWordsFilter:
            words = self.filterStopWords(words)

        # TODO
        # classify a list of words and return the 'pos' or 'neg' classification
        # Write code here
        


        attitude = 1
        pos_words = dict.copy(self.pos_words)
        neg_words = dict.copy(self.neg_words)
        pos_total = self.pos_total
        neg_total = self.neg_total


        # BEST MODEL
        if self.bestModel:
            
            alpha = int((len(pos_words) + len(neg_words)) / 5500)
            top_n = int((len(pos_words) + len(neg_words)) * 0.0025)
            
            if len(pos_words) > top_n and self.top_filter == 0:
                self.top_filter = sorted(zip(pos_words.values(),pos_words.keys()), reverse=True)[top_n][0]
            if len(neg_words) > top_n and self.top_filter_neg == 0:
                self.top_filter_neg = sorted(zip(neg_words.values(),neg_words.keys()), reverse=True)[top_n][0]

            for word in words:
                if word not in pos_words:
                    pos_words[word] = 0
                if word not in neg_words:
                    neg_words[word] = 0
            

            #print pos_total
            for word in pos_words:
                pos_words[word] += alpha
                pos_total += alpha

        
            for word in neg_words:
                neg_words[word] += alpha
                neg_total += alpha

            # REMOVE HIGH FREQ WORDS
            pos_occurLimit = self.top_filter
            neg_occurLimit = self.top_filter_neg

            p_pos = 0.0
            p_neg = 0.0

            vocab = defaultdict(int)

            for word in words:
                # FILTER
                if pos_words[word] > pos_occurLimit and neg_words[word] > neg_occurLimit:
                    continue
                if word not in vocab:
                    vocab[word] = 0
                else:
                    continue

                p_pos -= math.log(float(pos_words[word]) / pos_total)
                p_neg -= math.log(float(neg_words[word]) / neg_total)
        

            #  p(c) * pi(p(w|c))
            p_pos -= math.log(float(self.pos_rev)/(self.pos_rev+self.neg_rev))
            p_neg -= math.log(float(self.neg_rev)/(self.pos_rev+self.neg_rev))

            if p_pos > p_neg:
                return 'neg'

            return 'pos'
            
            

        for word in words:
            if word not in pos_words:
                pos_words[word] = 0
            if word not in neg_words:
                neg_words[word] = 0
            

	    alpha = 1

        # add one (alpha) smoothing
        vocab = defaultdict(int)
        for word in pos_words:
            pos_words[word] += alpha
            pos_total += alpha

        
        for word in neg_words:
            neg_words[word] += alpha
            neg_total += alpha

        p_pos = 0.0
        p_neg = 0.0

        vocab = defaultdict(int)

        # calculate pi(p(w|c))
        for word in words:
            # check duplicate word
            if self.naiveBayesBool:
                if word not in vocab:
                    vocab[word] = 0
                else:
                    continue
            
            p_pos -= math.log(float(pos_words[word]) / pos_total)
            p_neg -= math.log(float(neg_words[word]) / neg_total)
        

        #  p(c) * pi(p(w|c))
        p_pos -= math.log(float(self.pos_rev)/(self.pos_rev+self.neg_rev))
        p_neg -= math.log(float(self.neg_rev)/(self.pos_rev+self.neg_rev))

        if p_pos > p_neg:
            return 'neg'

        return 'pos'

    def addDocument(self, classifier, words):
        """
        Train your model on a document with label classifier (pos or neg) and words (list of strings). You should
        store any structures for your classifier in the naive bayes class. This function will return nothing
        """
        # TODO
        # Train model on document with label classifiers and words
        # Write code here

        vocab = defaultdict(int)

        for word in words:
            if self.naiveBayesBool:
                if word not in vocab:
                    vocab[word] = 0
                else:
                    continue
            
            if word not in self.pos_words:
                self.pos_words[word] = 0
            
            if word not in self.neg_words:
                self.neg_words[word] = 0
            
            if classifier == 'pos':
                self.pos_words[word] += 1
                self.pos_total += 1
            else:
                self.neg_words[word] += 1
                self.neg_total += 1

        if classifier == 'pos':    
            self.pos_rev += 1
        else:
            self.neg_rev += 1

        pass

    def readFile(self, fileName):
        """
        Reads a file and segments.
        """
        contents = []
        f = open(fileName)
        for line in f:
            contents.append(line)
        f.close()
        str = '\n'.join(contents)
        result = str.split()
        return result

    def trainSplit(self, trainDir):
        """Takes in a trainDir, returns one TrainSplit with train set."""
        split = self.TrainSplit()
        posDocTrain = os.listdir('%s/pos/' % trainDir)
        negDocTrain = os.listdir('%s/neg/' % trainDir)
        for fileName in posDocTrain:
            doc = self.Document()
            doc.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
            doc.classifier = 'pos'
            split.train.append(doc)
        for fileName in negDocTrain:
            doc = self.Document()
            doc.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
            doc.classifier = 'neg'
            split.train.append(doc)
        return split

    def train(self, split):
        for doc in split.train:
            words = doc.words
            if self.stopWordsFilter:
                words = self.filterStopWords(words)
            self.addDocument(doc.classifier, words)

    def crossValidationSplits(self, trainDir):
        """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
        splits = []
        posDocTrain = os.listdir('%s/pos/' % trainDir)
        negDocTrain = os.listdir('%s/neg/' % trainDir)
        # for fileName in trainFileNames:
        for fold in range(0, self.numFolds):
            split = self.TrainSplit()
            for fileName in posDocTrain:
                doc = self.Document()
                doc.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                doc.classifier = 'pos'
                if fileName[2] == str(fold):
                    split.test.append(doc)
                else:
                    split.train.append(doc)
            for fileName in negDocTrain:
                doc = self.Document()
                doc.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                doc.classifier = 'neg'
                if fileName[2] == str(fold):
                    split.test.append(doc)
                else:
                    split.train.append(doc)
            yield split

    def test(self, split):
        """Returns a list of labels for split.test."""
        labels = []
        for doc in split.test:
            words = doc.words
            if self.stopWordsFilter:
                words = self.filterStopWords(words)
            guess = self.classify(words)
            labels.append(guess)
        return labels

    def buildSplits(self, args):
        """
        Construct the training/test split
        """
        splits = []
        trainDir = args[0]
        if len(args) == 1:
            print '[INFO]\tOn %d-fold of CV with \t%s' % (self.numFolds, trainDir)

            posDocTrain = os.listdir('%s/pos/' % trainDir)
            negDocTrain = os.listdir('%s/neg/' % trainDir)
            for fold in range(0, self.numFolds):
                split = self.TrainSplit()
                for fileName in posDocTrain:
                    doc = self.Document()
                    doc.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                    doc.classifier = 'pos'
                    if fileName[2] == str(fold):
                        split.test.append(doc)
                    else:
                        split.train.append(doc)
                for fileName in negDocTrain:
                    doc = self.Document()
                    doc.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                    doc.classifier = 'neg'
                    if fileName[2] == str(fold):
                        split.test.append(doc)
                    else:
                        split.train.append(doc)
                splits.append(split)
        elif len(args) == 2:
            split = self.TrainSplit()
            testDir = args[1]
            print '[INFO]\tTraining on data set:\t%s testing on data set:\t%s' % (trainDir, testDir)
            posDocTrain = os.listdir('%s/pos/' % trainDir)
            negDocTrain = os.listdir('%s/neg/' % trainDir)
            for fileName in posDocTrain:
                doc = self.Document()
                doc.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                doc.classifier = 'pos'
                split.train.append(doc)
            for fileName in negDocTrain:
                doc = self.Document()
                doc.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                doc.classifier = 'neg'
                split.train.append(doc)

            posDocTest = os.listdir('%s/pos/' % testDir)
            negDocTest = os.listdir('%s/neg/' % testDir)
            for fileName in posDocTest:
                doc = self.Document()
                doc.words = self.readFile('%s/pos/%s' % (testDir, fileName))
                doc.classifier = 'pos'
                split.test.append(doc)
            for fileName in negDocTest:
                doc = self.Document()
                doc.words = self.readFile('%s/neg/%s' % (testDir, fileName))
                doc.classifier = 'neg'
                split.test.append(doc)
            splits.append(split)
        return splits

    def filterStopWords(self, words):
        """
        Stop word filter
        """
        removed = []
        for word in words:
            if not word in self.stopList and word.strip() != '':
                removed.append(word)
        return removed


def test10Fold(args, stopWordsFilter, naiveBayesBool, bestModel):
    nb = NaiveBayes()
    splits = nb.buildSplits(args)
    avgAccuracy = 0.0
    fold = 0
    for split in splits:
        classifier = NaiveBayes()
        classifier.stopWordsFilter = stopWordsFilter
        classifier.naiveBayesBool = naiveBayesBool
        classifier.bestModel = bestModel
        accuracy = 0.0
        for doc in split.train:
            words = doc.words
            classifier.addDocument(doc.classifier, words)

        for doc in split.test:
            words = doc.words
            guess = classifier.classify(words)
            if doc.classifier == guess:
                accuracy += 1.0

        accuracy = accuracy / len(split.test)
        avgAccuracy += accuracy
        print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy)
        fold += 1
    avgAccuracy = avgAccuracy / fold
    print '[INFO]\tAccuracy: %f' % avgAccuracy


def classifyFile(stopWordsFilter, naiveBayesBool, bestModel, trainDir, testFilePath):
    classifier = NaiveBayes()
    classifier.stopWordsFilter = stopWordsFilter
    classifier.naiveBayesBool = naiveBayesBool
    classifier.bestModel = bestModel
    trainSplit = classifier.trainSplit(trainDir)
    classifier.train(trainSplit)
    testFile = classifier.readFile(testFilePath)
    print classifier.classify(testFile)


def main():
    stopWordsFilter = False
    naiveBayesBool = False
    bestModel = False
    (options, args) = getopt.getopt(sys.argv[1:], 'fbm')
    if ('-f', '') in options:
        stopWordsFilter = True
    elif ('-b', '') in options:
        naiveBayesBool = True
    elif ('-m', '') in options:
        bestModel = True

    if len(args) == 2 and os.path.isfile(args[1]):
        classifyFile(stopWordsFilter, naiveBayesBool, bestModel, args[0], args[1])
    else:
        test10Fold(args, stopWordsFilter, naiveBayesBool, bestModel)


if __name__ == "__main__":
    main()
