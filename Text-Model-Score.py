#
# textmodel.py
#
#
# Name(s): Amar Kumar
#
#import string
import math
from porter import create_stem # type: ignore

class TextModel:
    """A class supporting complex models of text."""

    def __init__(self):
        """Create an empty TextModel."""
        # 
        # The text in the model, all in a single string--the original
        # and "cleaned" versions.
        #
        self.text = ''            # No text present yet
        self.cleanedtext = ''     # Nor any cleaned text yet
                                  # ..(cleaned == only letters, all lowercase)

        #
        # Create dictionaries for each characteristic
        #
        self.words = {}           # For counting words
        self.wordlengths = {}     # For counting word lengths
        self.stems = {}           # For counting stems
        self.sentencelengths = {} # For counting sentence lengths
        
        # Create another dictionary of your own
        #
        self.punct = {}     # For counting punctuations
        self.openers = {}   # For counting sentence openers
        self.sigwords = {}



    def __repr__(self):
        """Display the contents of a TextModel."""
        s = f'Words:\n{str(self.words)}\n\n'
        s += f'Word lengths:\n{str(self.wordlengths)}\n\n'
        s += f'Stems:\n{str(self.stems)}\n\n'
        s += f'Sentence lengths:\n{str(self.sentencelengths)}\n\n'
        s += f'Punctuations:\n{str(self.punct)}\n\n'
        s += f'Sentence Openers:\n{str(self.openers)}\n\n'
        s += f'Significant Words:\n{str(self.sigwords)}\n\n'
        #s += f'MY PARAMETER:\n{str(self.myparameter)}\n\n'
        s += '+'*75 + '\n'
        s += f'Text[:70]    {self.text[:70]}\n'
        s += f'Cleaned[:70] {self.cleanedtext[:70]}\n'
        s += '+'*75 + '\n\n'
        return s

    # We provide two text-adding methods (functions) here:
    def addRawText(self, text):
        """addRawText accepts self (the object itself)
                      and text, a string of raw text to add.
           Nothing is returned from this method, but
           the text _is_ added.
        """
        self.text += text 
        self.cleanedtext += self.cleanString(self.text) 

    # The second one adds text from a file:
    def addFileText(self, filename):
        """addFileText accepts a filename.
            
           Nothing is returned from this method, but
           the file is opened and its text _is_ added.

           If the file is not present, it will crash!
        """
        f = open(filename, 'r', encoding='utf-8')
                               # The above may need utf-8 or utf-16, depending
        text = f.read()        # Read all of the contents into text 
        f.close()              # Close the file
        self.addRawText(text)  # Uses the previous method!

    # Include other functions here.
    # In particular, you'll need functions that add to the model.

    def makeSentenceLengths(self):
        """Creates the dictionary of sentence lengths
               should use self.text, because it needs the punctuation!
        """

        LoW = self.text.split() 
        counter = 0
        for word in LoW:
            counter += 1
            if word[-1] in '.?!':
                if counter in self.sentencelengths:
                    self.sentencelengths[counter] += 1
                else: 
                    self.sentencelengths[counter] = 1
                counter = 0

    def makeWordLengths(self):
        """Creates the dictionary of word lengths
        """

        #LoW = self.text.split() 
        LoW = self.cleanString(self.text).split()
        #print(LoW)
        for word in LoW:
            counter = len(word)
            if counter in self.wordlengths:
                self.wordlengths[counter] += 1
            else: 
                self.wordlengths[counter] = 1


    def makeWords(self):
        """Creates the dictionary of words
        """

        #LoW = self.text.split() 
        LoW = self.cleanString(self.text).split()
        for word in LoW:
            if word in self.words:
                self.words[word] += 1
            else: 
                self.words[word] = 1

    def makeSigWords(self):
        """Creates the dictionary of significant words
        """

        #LoW = self.text.split() 
        LoW = self.cleanString(self.text).split()
        common = ['the', 'be', 'to', 'of', 'and', 'a', 'an', 'in', 'as', 'at']
        for word in LoW:
            if word not in common:
                if word in self.sigwords:
                    self.sigwords[word] += 1
                else: 
                    self.sigwords[word] = 1

    def makeStems(self):
        """Creates the dictionary of words
        """

        #LoW = self.text.split() 
        LoW = self.cleanString(self.text).split()
        for word in LoW:
            stem = create_stem(word)
            if stem in self.stems:
                self.stems[stem] += 1
            else: 
                self.stems[stem] = 1
    
    
    def makePunctuation(self):
        """Creates the dictionary of words
        """
        punctuation = '!?.,\''

        for c in self.text:  # c is each character
        # Use the Python string library
            if c in punctuation:
                if c in self.punct:
                    self.punct[c] += 1
                else: 
                    self.punct[c] = 1
            
    def makeSentenceOpener(self):
        """Creates the dictionary of sentence openers
        """
        LoW = self.text.split()
        opener = LoW[0]
        self.openers[opener] = 1 
        for word in LoW:
            if word[-1] in '.?!':
                ind = LoW.index(word)
                try:
                    opener = LoW[ind+1]
                except:
                    continue
                if opener in self.openers:
                    self.openers[opener] += 1
                else: 
                    self.openers[opener] = 1
            
    
    def cleanString(self, s):
        """Returns the string s, but
           with only ASCII characters, only lowercase, and no punctuation.
           See the description and hints in the problem!
        """
        
        new_text = ''

        s = s.encode("ascii", "ignore")   # Ignores non-ASCII characters
        s = s.decode()         # Decodes it back to a string (with the non-ACSII characters removed) 

        result = s.lower()    # Convert s to lower-cases

        punctuation = '!?.,\'\"'

        for c in result:  # c is each character
        # Use the Python string library
            if c in punctuation:
                new_text += ''
            else:
                new_text += c
    
        return new_text

    def createAllDictionaries(self):
        """Create out all five of self's
           dictionaries in full.
        """
        self.makeSentenceLengths()
        self.sentencelengths = dict(sorted(self.sentencelengths.items()))
        self.makeWords()
        self.words = dict(sorted(self.words.items()))
        self.makeStems()
        self.stems = dict(sorted(self.stems.items()))
        self.makeWordLengths()
        self.wordlengths = dict(sorted(self.wordlengths.items()))
        self.makePunctuation()
        self.punct = dict(sorted(self.punct.items()))
        self.makeSentenceOpener()
        self.openers = dict(sorted(self.openers.items()))
        self.makeSigWords()
        self.sigwords = dict(sorted(self.sigwords.items()))

    def normalizeDictionary(self, d):
        """
        Accepts a dictionary d and 
        returns a normalized version of the dictionary, i.e., one in which the values add up to 1.0. 
        """
        nd = d.copy()
        sumvals = sum(d.values())
        for k in d:
            
            nd[k] = d[k]/sumvals
        return nd
    
    def smallestValue(self, nd1, nd2):
        """
        Accepts any two model dictionaries nd1 and nd2 and
        returns the smallest positive (non-zero) value across them both.
        """
        vals = list(nd1.values()) + list(nd2.values())
        vals = [i for i in vals if i != 0]
        return min(vals)
    
    def compareDictionaries(self, d, nd1, nd2):
        """
        Computes:
        The log-probability that the dictionary d arose from the 
        distribution of data in the normalized dictionary nd1.
        The log-probability that dictionary d arose from the 
        distribution of data in normalized dictionary nd2.
        Return both of these log-probability values in a list [lp1, lp2]
        """

        epsilon = 0.5*(self.smallestValue(nd1, nd2))

        #if sum(nd1.values()) != 1 or sum(nd2.values()) != 1:
            #return [0,0]
        
        total_log_prob_nd1 = 0.0
        for k in d:
            if k in nd1:
                total_log_prob_nd1 += d[k]*math.log(nd1[k])
            else:
                total_log_prob_nd1 += d[k]*math.log(epsilon)

        total_log_prob_nd2 = 0.0
        for k in d:
            if k in nd2:
                total_log_prob_nd2 += d[k]*math.log(nd2[k])
            else:
                total_log_prob_nd2 += d[k]*math.log(epsilon)

        return [total_log_prob_nd1, total_log_prob_nd2]

        
    def compareDictionaries1(self, d, nd1, nd2, type):
        """
        Computes:
        The log-probability that the dictionary d arose from the 
        distribution of data in the normalized dictionary nd1.
        The log-probability that dictionary d arose from the 
        distribution of data in normalized dictionary nd2.
        Return both of these log-probability values in a list [lp1, lp2]
        """

        epsilon = 0.5*(self.smallestValue(nd1, nd2))
        weight = 0

        if type == 1:
            weight = 1
        elif type == 2:
            weight = 1
        elif type == 3:
            weight = 0
        elif type == 4:
            weight = 5
        elif type == 5:
            weight = 2
        elif type == 6:
            weight = 1
        elif type == 7:
            weight = 3
        else:
            weight = 0

        #if sum(nd1.values()) != 1 or sum(nd2.values()) != 1:
            #return [0,0]
        
        total_log_prob_nd1 = 0.0
        for k in d:
            if k in nd1:
                total_log_prob_nd1 += weight*d[k]*math.log(nd1[k])
            else:
                total_log_prob_nd1 += weight*d[k]*math.log(epsilon)

        total_log_prob_nd2 = 0.0
        for k in d:
            if k in nd2:
                total_log_prob_nd2 += weight*d[k]*math.log(nd2[k])
            else:
                total_log_prob_nd2 += weight*d[k]*math.log(epsilon)

        return [total_log_prob_nd1, total_log_prob_nd2]

        
    
    def compareTextWithTwoModels(self, model1, model2):
        """
        Runs the compareDictionaries method, for each of the feature dictionaries in self 
        against the corresponding (normalized) dictionaries in model1 and model2.
        """

        model1score = 0
        model2score = 0

        print(f"     {'name':>20s}   {'vsTM1':>10s}   {'vsTM2':>10s} ")
        print(f"     {'----':>20s}   {'-----':>10s}   {'-----':>10s} ")
        d_name = 'Words'
        nd1 = self.normalizeDictionary(model1.words)
        nd2 = self.normalizeDictionary(model2.words)
        #LogProbs1 = self.compareDictionaries(self.words, nd1, nd2)
        LogProbs1 = self.compareDictionaries1(self.words, nd1, nd2, 1)
        if LogProbs1[0] > LogProbs1[1]:
            model1score += 1
        elif LogProbs1[0] < LogProbs1[1]:
            model2score += 1
        print(f"     {d_name:>20s}   {LogProbs1[0]:>10.2f}   {LogProbs1[1]:>10.2f} ") 
        d_name = 'Word Lengths'
        nd1 = self.normalizeDictionary(model1.wordlengths)
        nd2 = self.normalizeDictionary(model2.wordlengths)
        #LogProbs1 = self.compareDictionaries(self.wordlengths, nd1, nd2)
        LogProbs1 = self.compareDictionaries1(self.wordlengths, nd1, nd2, 2)
        if LogProbs1[0] > LogProbs1[1]:
            model1score += 1
        elif LogProbs1[0] < LogProbs1[1]:
            model2score += 1
        print(f"     {d_name:>20s}   {LogProbs1[0]:>10.2f}   {LogProbs1[1]:>10.2f} ") 
        d_name = 'Stems'
        nd1 = self.normalizeDictionary(model1.stems)
        nd2 = self.normalizeDictionary(model2.stems)
        #LogProbs1 = self.compareDictionaries(self.stems, nd1, nd2)
        LogProbs1 = self.compareDictionaries1(self.stems, nd1, nd2, 3)
        if LogProbs1[0] > LogProbs1[1]:
            model1score += 1
        elif LogProbs1[0] < LogProbs1[1]:
            model2score += 1
        print(f"     {d_name:>20s}   {LogProbs1[0]:>10.2f}   {LogProbs1[1]:>10.2f} ") 
        d_name = 'Sentence Lengths'
        nd1 = self.normalizeDictionary(model1.sentencelengths)
        nd2 = self.normalizeDictionary(model2.sentencelengths)
        #LogProbs1 = self.compareDictionaries(self.sentencelengths, nd1, nd2)
        LogProbs1 = self.compareDictionaries1(self.sentencelengths, nd1, nd2, 4)
        if LogProbs1[0] > LogProbs1[1]:
            model1score += 1
        elif LogProbs1[0] < LogProbs1[1]:
            model2score += 1
        print(f"     {d_name:>20s}   {LogProbs1[0]:>10.2f}   {LogProbs1[1]:>10.2f} ")
        d_name = 'Punctuation'
        nd1 = self.normalizeDictionary(model1.punct)
        nd2 = self.normalizeDictionary(model2.punct)
        #LogProbs1 = self.compareDictionaries(self.punct, nd1, nd2)
        LogProbs1 = self.compareDictionaries1(self.punct, nd1, nd2, 5)
        if LogProbs1[0] > LogProbs1[1]:
            model1score += 1
        elif LogProbs1[0] < LogProbs1[1]:
            model2score += 1
        print(f"     {d_name:>20s}   {LogProbs1[0]:>10.2f}   {LogProbs1[1]:>10.2f} ")
        d_name = 'Sentence Openers'
        nd1 = self.normalizeDictionary(model1.openers)
        nd2 = self.normalizeDictionary(model2.openers)
        #LogProbs1 = self.compareDictionaries(self.openers, nd1, nd2)
        LogProbs1 = self.compareDictionaries1(self.openers, nd1, nd2, 6)
        if LogProbs1[0] > LogProbs1[1]:
            model1score += 1
        elif LogProbs1[0] < LogProbs1[1]:
            model2score += 1
        print(f"     {d_name:>20s}   {LogProbs1[0]:>10.2f}   {LogProbs1[1]:>10.2f} ")
        d_name = 'Significant Words'
        nd1 = self.normalizeDictionary(model1.sigwords)
        nd2 = self.normalizeDictionary(model2.sigwords)
        #LogProbs1 = self.compareDictionaries(self.sigwords, nd1, nd2)
        LogProbs1 = self.compareDictionaries1(self.sigwords, nd1, nd2, 7)
        if LogProbs1[0] > LogProbs1[1]:
            model1score += 1
        elif LogProbs1[0] < LogProbs1[1]:
            model2score += 1
        print(f"     {d_name:>20s}   {LogProbs1[0]:>10.2f}   {LogProbs1[1]:>10.2f} ") 

        print('---> Model 1 wins on ', model1score, 'features.')
        print('---> Model 2 wins on ', model2score, 'features.')

        if model1score > model2score:
            print('++++    Model1 is the better match!    ++++')
        elif model1score < model2score:
            print('++++    Model2 is the better match!    ++++')
        else:
            print('++++    Both Models are the same!    ++++')
        

# TRAINING TEXTS
TM_Sawyer = TextModel()
TM_Sawyer.addFileText("Sawyer.txt")
TM_Sawyer.createAllDictionaries()  # provided in hw description

TM_Harry = TextModel()
TM_Harry.addFileText("HarryPotter.txt")
TM_Harry.createAllDictionaries()  # provided in hw description

# TEST TEXTS
TM_Harry2 = TextModel()
TM_Harry2.addFileText("HarryPotter2.txt")
TM_Harry2.createAllDictionaries()  # provided in hw description

TM_AmarFWS = TextModel()
TM_AmarFWS.addFileText("FWSEssay.txt")
TM_AmarFWS.createAllDictionaries()  # provided in hw description

TM_WashPost = TextModel()
TM_WashPost.addFileText("WashingtonPost.txt")
TM_WashPost.createAllDictionaries()  # provided in hw description

#Comparisons

print('Comparing HarryPotter2 with HarryPotter and Tom Sawyer')
TM_Harry2.compareTextWithTwoModels(TM_Harry, TM_Sawyer)
print('\n')

print('Comparing my FWS Essay with HarryPotter and Tom Sawyer')
TM_AmarFWS.compareTextWithTwoModels(TM_Harry, TM_Sawyer)
print('\n')

print('Comparing a Washington Post article with HarryPotter and Tom Sawyer')
TM_WashPost.compareTextWithTwoModels(TM_Harry, TM_Sawyer)
print('\n')



