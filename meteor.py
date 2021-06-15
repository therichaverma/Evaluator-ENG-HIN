import snowballstemmer
import re, nltk
from home.HindiSyns import *
stemmer = snowballstemmer.stemmer('hindi')

#Output = open("C:\\Users\\91742\\Desktop\\Output(1 Sent).txt", encoding="utf8").read()
#Reference = open("C:\\Users\\91742\\Desktop\\Reference(1 Sent).txt", encoding="utf8").read()

#hyp = nltk.word_tokenize(Output)
#ref = nltk.word_tokenize(Reference)


def rm_matched(dic, r, h):
    for i in dic.values():  # removing exactly matched elements from hypotheses
        x = re.split("\s", i, 1)
        # print(x[0],x[1])
        h.remove(x[0])
    for i in dic.keys():  # removing exactly matched elements from references
        x = re.split("\s", i, 1)
        # print(x[0], x[1])
        r.remove(x[0])
    return r, h
def exact_match(r, h, lr, lh):
    chunks = []
    exa = []
    exact = {}
    s = 0
    for i in range(0, lr):
        for j in range(s, lh):
            if r[i] == h[j]:
                if r[i] + str(i) not in exact:
                    exa.append(r[i] + str(i))
                    if r[i] + " " + str(i) not in exact.keys():
                        if h[j] + " " + str(j) not in exact.values():
                            exact.update({r[i] + " " + str(i): h[j] + " " + str(j)})
                    s = i + 1
                    break
            elif r[i] != h[j]:
                if len(exa) > 1:
                    chunks.append(list(exa))
                exa.clear()
    r, h = rm_matched(exact, r, h)
    return len(exact), r, h, len(chunks)

# print(rr)
# print(hh)

def stem_match(r, h, lr, lh):
    stems = {}
    stem_l = []
    chunks = []
    s = 0
    for i in range(0, lr):
        for j in range(s, lh):
            if stemmer.stemWord(r[i]) == stemmer.stemWord(h[j]):
                if r[i] + " " + stemmer.stemWord(r[i]) + " " + str(i) not in stems.keys():
                    if h[j] + " " + stemmer.stemWord(h[j]) + " " + str(j) not in stems.values():
                        stems.update(
                            {r[i] + " " + stemmer.stemWord(r[i]) + " " + str(i): h[j] + " " + stemmer.stemWord(
                                h[j]) + " " + str(j)})
                        stem_l.append(r[i] + str(i))
                    s = i + 1
                    break
            elif r[i] != h[j]:
                if len(stem_l) > 1:
                    chunks.append(list(stem_l))
                stem_l.clear()

    r, h = rm_matched(stems, r, h)
    return len(stems), r, h, len(chunks)


# print(rrr)
# print(hhh)

def syn_match(r, h, lr, lh):
    synonym = {}
    syn_l = []
    chunks = []
    for i in range(0, lr):
        if syns(r[i]):
            synss = syns(r[i])
            for j in range(0, lh):
                if h[j] in synss:
                    synonym.update({r[i] + str(i): h[j] + str(j)})
                    syn_l.append(r[i] + str(i))
                    break
                else:
                    if len(syn_l) > 1:
                        chunks.append(list(syn_l))
                    syn_l.clear()

    return len(synonym), len(chunks)

def meteor_score(hyp,ref):
    len_exact, rr, hh, exact_chunks = exact_match(ref, hyp, len(ref), len(hyp))
    len_stem, rrr, hhh, stem_chunks = stem_match(rr, hh, len(rr), len(hh))
    len_syn, syn_chunks = syn_match(rrr, hhh, len(rrr), len(hhh))
    print("length hyp",len(hyp))
    try:
        precision = round((len_exact + len_stem + len_syn) / len(hyp), 4)
        recall = round(((len_exact + len_stem + len_syn) / len(ref)), 4)
        Harmonic_Mean = round((10 * precision * recall) / (recall + (9 * precision)), 4)
    except:
        precision = 0
        recall = 0
        Harmonic_Mean = 0
    print("Harmonic mean=", Harmonic_Mean)
    chunks = exact_chunks + stem_chunks + syn_chunks
    unigram_match = len_exact + len_stem + len_syn
    try:
        penality = round((0.5 * ((chunks / unigram_match) ** 3)), 4)
    except:
        penality=0
    print("penalty =", penality)
    score = Harmonic_Mean * (1 - penality)
    if score > 1 or score == 1:
        score = score/10
    elif score > 10 or score == 10:
        score = score / 100
    elif score > 100 or score == 100:
        score = score / 1000
    print("M score=",score)
    return round(score,4)


#print(meteor_score(hyp,ref))