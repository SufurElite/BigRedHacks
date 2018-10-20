import os, re

def getAverageSentenceLength(text):
    wordcounts = []
    sentences = text.split('.')
    for sentence in sentences:
        words = sentence.split(' ')
        wordcounts.append(len(words))
    average_wordcount = sum(wordcounts)/len(wordcounts)
    return average_wordcount;

def getAverageParentheticals(text):
    return text.count("(");

def getNumberOfDependentClauses(text):
    sentences = text.split('.')

    Fanboys = ["for", "and", "nor", "but", "or", "yet", "so",
              "moreover", "however", "consequently", "indeed", "nevertheless",
              "therefore"]
    count = 0;
    for sentence in sentences:
        words = sentence.split(' ')
        if(sentence.count(",")>0):
            word = sentence.partition(',')[-1].split()[0]
            if(word not in Fanboys):
                count+=1;
            #print(words[1])
    return count;

def numOfSemiColons(text):
    return text.count(";")

def getTopBigrams(text):
    Bigrams = {}
    text = text.replace('.', ' ').replace('(',' ').replace(')', ' ').replace(',', ' ').replace('?',' ').replace('!', ' ').replace('[', ' ').replace(']', ' ')
    text = text.replace(';', ' ').replace(':', ' ')
    no_num_text = ''.join(i for i in text if not i.isdigit())
    import nltk
    from nltk.tokenize import word_tokenize
    tokens = nltk.word_tokenize(text)
    bigrm = nltk.bigrams(tokens)
    fdist = nltk.FreqDist(bigrm)
    words = nltk.tokenize.word_tokenize(text)
    fdist2 = nltk.FreqDist(words)
    i = 0
    for k,v in fdist2.items():
        print(k)
        print(v)
    input()
    Bigrams = list(bigrm)
    print(Bigrams)
    return Bigrams;

def getTopTrigrams(text):
    Trigrams = []
    return Trigrams;
def getLexicalDiversity(text):
    return len(set(text)) / len(text)

def statForEssay(name, subdir, t_file):
    file = open(subdir+"\\"+t_file, "r",encoding='utf-8', errors='ignore')
    Stats = [];
    Stats.append(name);
    Stats.append(subdir+"\\"+t_file)
    text = file.read()
    Stats.append(getAverageSentenceLength(text))
    Stats.append(getAverageParentheticals(text))
    Stats.append(getNumberOfDependentClauses(text))
    Stats.append(numOfSemiColons(text))
    Stats.append(getLexicalDiversity(text))
    return Stats;

def isSameAsNext(Essay_Stats, i):
    if(i!=len(Essay_Stats)-1):
        if(Essay_Stats[i][0]==Essay_Stats[i+1][0]):
            return True;

    return False;

def Average_Stats(Essay_Stats):

    text_corpus = " "
    BigramsAndTrigrams = []
    count = 1;
    for i in range(len(Essay_Stats)):
        if isSameAsNext(Essay_Stats, i):
            file = open(Essay_Stats[i][1], "r",encoding='utf-8', errors='ignore')
            text_corpus+=file.read() + " ";
            count+=1;
        else:
            file = open(Essay_Stats[i][1], "r",encoding='utf-8', errors='ignore')
            print(Essay_Stats[i][0])
            print(count)
            text_corpus+=file.read() + " ";
            Essay_Stats[i].append(count)
            Essay_Stats[i].append(getTopBigrams(text_corpus))
            Essay_Stats[i].append(getTopTrigrams(text_corpus))
            text_corpus = ""
            count = 1;
    return None;


def writeAverageStats(Average_Stats):
    return True;
def createStats():
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\Docs"
    curr_person = ""
    Essay_stats = []
    for subdir, dirs, files in os.walk(dir_path):
        if(subdir!=curr_person and subdir[-4:]!="Docs"):
            curr_person = subdir;
        for file in files:
            Essay_stats.append(statForEssay(curr_person, subdir, file));
            #print(os.path.join(subdir, file))
    print("\n")
    average_stats = Average_Stats(Essay_stats)

    for i in range(len(Essay_stats)):
        for j in range(len(Essay_stats[i])):
            print(str(Essay_stats[i][j]))


    return None;
