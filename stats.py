import os, re, nltk, json
from nltk.tokenize import word_tokenize

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
        if(sentence.count(",")>1):
            word = sentence.partition(',')[-1].split()[0]
            if(word not in Fanboys):
                count+=1;
            #print(words[1])
    return count;

def numOfSemiColons(text):
    return text.count(";")

def getVocab(text):
    words = nltk.tokenize.word_tokenize(text)
    vocab_dist = nltk.FreqDist(words)
    vocab = []
    for k, v in vocab_dist.items():
        vocab.append((k,v))
    vocab.sort(key=lambda tup: tup[1])
    vocab = vocab[-100:]
    return vocab;

def getTopBigrams(text):
    text = text.replace('.', ' ').replace('(',' ').replace(')', ' ').replace(',', ' ').replace('?',' ').replace('!', ' ').replace('[', ' ').replace(']', ' ')
    text = text.replace(';', ' ').replace(':', ' ')
    no_num_text = ''.join(i for i in text if not i.isdigit())

    tokens = nltk.word_tokenize(text)
    bigrm = nltk.bigrams(tokens)
    fdist = nltk.FreqDist(bigrm)
    Bigrams = []
    for k, v in fdist.items():
        Bigrams.append((k,v))
    Bigrams.sort(key=lambda tup: tup[1])
    Bigrams = Bigrams[-50:]
    return Bigrams;

def getTopTrigrams(text):
    text = text.replace('.', ' ').replace('(',' ').replace(')', ' ').replace(',', ' ').replace('?',' ').replace('!', ' ').replace('[', ' ').replace(']', ' ')
    text = text.replace(';', ' ').replace(':', ' ')
    no_num_text = ''.join(i for i in text if not i.isdigit())

    tokens = nltk.word_tokenize(text)
    bigrm = nltk.trigrams(tokens)
    fdist = nltk.FreqDist(bigrm)
    Trigrams = []
    for k, v in fdist.items():
        Trigrams.append((k,v))
    Trigrams.sort(key=lambda tup: tup[1])
    Trigrams = Trigrams[-50:]
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
    Average_Stats = []
    BigramsAndTrigrams = []
    count = 1;
    average_sentence_length = 0;
    average_parentheticals = 0;
    average_dependent = 0;
    average_semicolons = 0;
    average_lexicalDiversity = 0;
    for i in range(len(Essay_Stats)):
        if isSameAsNext(Essay_Stats, i):
            average_sentence_length+=Essay_Stats[i][2]
            average_parentheticals+=Essay_Stats[i][3]
            average_dependent+=Essay_Stats[i][4]
            average_semicolons+=Essay_Stats[i][5]
            average_lexicalDiversity+=Essay_Stats[i][6]
            file = open(Essay_Stats[i][1], "r",encoding='utf-8', errors='ignore')
            text_corpus+=file.read().lower() + " ";
            count+=1;
        else:
            temp = []

            temp.append(Essay_Stats[i][0])
            average_sentence_length+=Essay_Stats[i][2]
            average_parentheticals+=Essay_Stats[i][3]
            average_dependent+=Essay_Stats[i][4]
            average_semicolons+=Essay_Stats[i][5]
            average_lexicalDiversity+=Essay_Stats[i][6]

            temp.append(average_sentence_length/count)
            temp.append(average_parentheticals/count)
            temp.append(average_dependent/count)
            temp.append(average_semicolons/count)
            temp.append(average_lexicalDiversity/count)
            file = open(Essay_Stats[i][1], "r",encoding='utf-8', errors='ignore')
            text_corpus+=file.read().lower() + " ";
            temp.append(getLexicalDiversity(text_corpus))
            temp.append(count)
            temp.append(getVocab(text_corpus))
            temp.append(getTopBigrams(text_corpus))
            temp.append(getTopTrigrams(text_corpus))
            Average_Stats.append(temp)

            text_corpus = ""
            count = 1;
            average_sentence_length = 0;
            average_parentheticals = 0;
            average_dependent = 0;
            average_semicolons = 0;
            average_lexicalDiversity = 0;

    return Average_Stats;


def writeAverageStats(Average_Stats, JSON_Avg_Paths):
    for i in range(len(Average_Stats)):
        name = Average_Stats[i][0][Average_Stats[i][0].rfind('\\')+1:]
        f = open(Average_Stats[i][0]+"\\"+name+"AvgStats.json", 'w')
        temp = []
        temp.append(name)
        temp.append(Average_Stats[i][0]+"\\"+name+"AvgStats.json")
        JSON_Avg_Paths.append(temp)
        count = Average_Stats[i][7]
        f.write("{\n\"Name\":\""+name+"\",")
        f.write("\n\"Number of Essays\":"+str(count)+",")
        f.write("\n\"Average Sentence Length\":"+str(Average_Stats[i][1])+",")
        f.write("\n\"Average # of Parentheticals\":"+str(Average_Stats[i][2])+",")
        f.write("\n\"Average # of dependent clauses\":"+str(Average_Stats[i][3])+",")
        f.write("\n\"Average # of Semicolons\":"+str(Average_Stats[i][4])+",")
        f.write("\n\"Average Essay Lexical Diversity\":"+str(Average_Stats[i][5])+",")
        f.write("\n\"Average Total Lexical Diversity\":"+str(Average_Stats[i][6])+",")
        f.write("\n\"Vocabulary\":[")
        for j in range(len(Average_Stats[i][8])):
            if(j!=len(Average_Stats[i][8])-1):
                f.write("\""+Average_Stats[i][8][j][0]+"\",")
            else:
                f.write("\""+Average_Stats[i][8][j][0]+"\"],")
        f.write("\n\"Vocabulary Frequency\":[\n")
        for j in range(len(Average_Stats[i][8])):
            if(j!=len(Average_Stats[i][8])-1):
                f.write(str(Average_Stats[i][8][j][1]/count)+",")
            else:
                f.write(str(Average_Stats[i][8][j][1]/count)+"\n],")
        f.write("\n\"Bigram\":[\n")
        for j in range(len(Average_Stats[i][9])):
            if(j!=len(Average_Stats[i][9])-1):
                f.write("\""+Average_Stats[i][9][j][0][0]+" "+Average_Stats[i][9][j][0][1]+"\",")
            else:
                f.write("\""+Average_Stats[i][9][j][0][0]+" "+Average_Stats[i][9][j][0][1]+"\"],")
        f.write("\n\"Bigram Frequency\":[\n")
        for j in range(len(Average_Stats[i][9])):
            if(j!=len(Average_Stats[i][9])-1):
                f.write(str(Average_Stats[i][9][j][1]/count)+",")
            else:
                f.write(str(Average_Stats[i][9][j][1]/count)+"\n],")
        f.write("\n\"Trigram\":[\n")
        for j in range(len(Average_Stats[i][10])):
            if(j!=len(Average_Stats[i][10])-1):
                f.write("\""+Average_Stats[i][10][j][0][0]+" "+Average_Stats[i][10][j][0][1]+" "+Average_Stats[i][10][j][0][2]+"\",")
            else:
                f.write("\""+Average_Stats[i][10][j][0][0]+" "+Average_Stats[i][10][j][0][1]+" "+Average_Stats[i][10][j][0][2]+"\"],")
        f.write("\n\"Trigram Frequency\":[\n")
        for j in range(len(Average_Stats[i][10])):
            if(j!=len(Average_Stats[i][10])-1):
                f.write(str(Average_Stats[i][10][j][1]/count)+",")
            else:
                f.write(str(Average_Stats[i][10][j][1]/count)+"\n]\n}")
    return True;



def CreateDifferentials(Target_Data, Given_Values, i):
    name = Given_Values[i][0][Given_Values[i][0].rfind('\\')+1:]

    if(Target_Data['Name']==name):
        Target=1
    else:
        Target=0
    diffInSentenceLength = Target_Data['Average Sentence Length']-Given_Values[i][2]
    diffInParentheticals = Target_Data['Average # of Parentheticals']-Given_Values[i][3]
    diffInDependent = Target_Data['Average # of dependent clauses']-Given_Values[i][4]
    diffInSemicolons = Target_Data['Average # of Semicolons']-Given_Values[i][5]
    diffInEssayLexicalDiversity = Target_Data['Average Essay Lexical Diversity']-Given_Values[i][6]
    diffInTotalLexicalDiversity = Target_Data['Average Total Lexical Diversity']-Given_Values[i][6]
    file = open(Given_Values[i][1], "r",encoding='utf-8', errors='ignore')
    text= file.read()
    X_Vocab = getVocab(text);
    Y_Vocab = Target_Data['Vocabulary']
    X_Bigrams = getTopBigrams(text)
    Y_Bigrams = Target_Data['Bigram']
    X_Trigram = getTopTrigrams(text)
    Y_Trigram = Target_Data['Trigram']
    vocab_percentage = 0;
    for i in range(len(Y_Vocab)):
        if(Y_Vocab[i]==X_Vocab[i][0]):
            vocab_percentage+=1;
    vocab_percentage/=len(Y_Vocab);
    bigram_percentage = 0;
    for i in range(len(Y_Bigrams)):
        if(Y_Bigrams[i][0]==X_Bigrams[i][0]):
            bigram_percentage+=1;
    bigram_percentage/=len(Y_Bigrams)
    trigram_percentage = 0;
    for i in range(len(Y_Trigram)):
        if(Y_Trigram[i]==X_Trigram[i][0]):
            trigram_percentage+=1;
    trigram_percentage/=len(Y_Trigram);
    X = [diffInSentenceLength,diffInParentheticals,diffInDependent,diffInSemicolons, diffInEssayLexicalDiversity,diffInTotalLexicalDiversity, vocab_percentage, bigram_percentage, trigram_percentage]
    return X, Target;

def WriteTrainingJson(path, X_Values, Target):
    file = open(path, 'w')
    file.write("{\n\t\"Title\":\"Starting Dataset\",")
    file.write("\n\t\"Desc\":\"Dataset based on statistics from essays for the BigRedHackathon\",")
    file.write("\n\t\"Data\":[")
    for i in range(len(X_Values)):
        if(i!=len(X_Values)-1):
            file.write(str(X_Values[i])+",")
        else:
            file.write(str(X_Values[i])+"\n],")
    file.write("\n\t\"Target\":[")
    for i in range(len(Target)):
        if(i!=len(Target)-1):
            file.write(str(Target[i])+",")
        else:
            file.write(str(Target[i])+"\n]\n}")
    return None;

def CreateInput(JSON_Avg_Paths):
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\Docs"
    curr_person = ""
    Essay_Stats = []
    for subdir, dirs, files in os.walk(dir_path):
        if(subdir!=curr_person and subdir[-4:]!="Docs"):
            curr_person = subdir;
        for file in files:
            if(file[-4:]!="json"):
                Essay_Stats.append(statForEssay(curr_person, subdir, file));
    Target = []
    X_Values = []
    for i in range(len(JSON_Avg_Paths)):
        with open(JSON_Avg_Paths[i][1]) as j_file:
            data = json.load(j_file)
        for j in range(len(Essay_Stats)):
            temp_X=[]
            temp_Y=0
            temp_X, temp_Y=CreateDifferentials(data,Essay_Stats, j)
            X_Values.append(temp_X)
            Target.append(temp_Y)
    WriteTrainingJson(dir_path+"\\startingDataset.json",X_Values, Target)
    print(X_Values)
    print(Target)
    return None;

def createStats(inputFile):
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\Docs"
    curr_person = ""
    Essay_stats = []
    for subdir, dirs, files in os.walk(dir_path):
        if(subdir!=curr_person and subdir[-4:]!="Docs"):
            curr_person = subdir;
        for file in files:
            if(file[-4:]!="json"):
                Essay_stats.append(statForEssay(curr_person, subdir, file));
            #print(os.path.join(subdir, file))
    print("\n")
    average_stats = Average_Stats(Essay_stats)
    '''
    for i in range(len(average_stats)):
        for j in range(len(average_stats[i])):
            print(str(average_stats[i][j]))
    '''
    JSON_Avg_Paths = []
    writeAverageStats(average_stats, JSON_Avg_Paths);
    if(inputFile):
        CreateInput(JSON_Avg_Paths);
    return None;
