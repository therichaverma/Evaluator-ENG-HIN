from functools import reduce
import  operator
import nltk, math
from collections import Counter

#Output = open("C:\\Users\\91742\\Desktop\\Output(1 Sent).txt", encoding="utf8")
#Reference = open("C:\\Users\\91742\\Desktop\\Reference(1 Sent).txt", encoding="utf8")


#print("Hypothesis =", hyp)
#print("Reference=", ref)
#print(len(hyp), len(ref))


def tokens(hypothesis, reference):
    for i in hypothesis:
        i = i.lstrip("['")
        i = i.rstrip("]'")
        # print(sentences)
        h_sen = nltk.word_tokenize(i)
        # print(sentences)

        for j in reference:
            j = j.lstrip("['")
            j = j.rstrip("]'")
            # print(sentences)
            r_sen = nltk.word_tokenize(j)
            # print(sentences)
    return h_sen, r_sen


def bigram_words(hyp,ref):
    hyp_bigram=[]
    ref_bigram=[]
    for i in range(0,len(hyp)-1):
        hyp_bigram.append(hyp[i]+" "+hyp[i+1])
    for i in range(0,len(ref)-1):
        ref_bigram.append(ref[i]+" "+ref[i+1])
    return hyp_bigram, ref_bigram


def trigram_words(hyp,ref):
    hyp_trigram = []
    ref_trigram = []
    for i in range(0, len(hyp) - 2):
        hyp_trigram.append(hyp[i] + " " + hyp[i + 1] + " " + hyp[i + 2])
    for i in range(0, len(ref) - 2):
        ref_trigram.append(ref[i] + " " + ref[i + 1] + " " + ref[i + 2])
    return hyp_trigram, ref_trigram


def fourgram_words(hyp,ref):
    hyp_fourgram = []
    ref_fourgram = []
    for i in range(0, len(hyp) - 3):
        hyp_fourgram.append(hyp[i] + " " + hyp[i + 1] + " " + hyp[i + 2] + " " + hyp[i + 3])
    for i in range(0, len(ref) - 3):
        ref_fourgram.append(ref[i] + " " + ref[i + 1] + " " + ref[i + 2] + " " + ref[i + 3])
    return hyp_fourgram, ref_fourgram


def count_hypothesis(unigram,bigram,trigram,fourgram):
    c_unigram = 0
    c_bigram = 0
    c_trigram = 0
    c_fourgram = 0
    count_uni = Counter(unigram)
    count_bi = Counter(bigram)
    count_tri = Counter(trigram)
    count_four = Counter(fourgram)
    for i in count_uni.values():
        c_unigram = c_unigram+int(i)
    for i in count_bi.values():
        c_bigram = c_bigram+int(i)
    for i in count_tri.values():
        c_trigram = c_trigram+int(i)
    for i in count_four.values():
        c_fourgram = c_fourgram+int(i)

    return count_uni, count_bi, count_tri, count_four, c_unigram, c_bigram, c_trigram, c_fourgram


def ref_match(h,r,lh,lr):
    ref_count = {}
    c = 0
    for i in range(0, lh):
        for j in range(0, lr):
            if h[i] == r[j] :
                c += 1
            else:
                c += 0
        ref_count.update({h[i]:c})
        c = 0
    return ref_count


def min_count(count,ref_count):
    global a
    min_c=[]
    for k,v in ref_count.items():
        for kk,vv in count.items():
            if k == kk:
                a= vv
        min_c.append(min(int(a),int(v)))
    return min_c

def geometric_mean(precisions):
    return (reduce(operator.mul, precisions)) ** (1.0 / len(precisions))


def bp(hyp,ref):
    if hyp > ref:
        bp = 1
    else:
        bp = math.exp(1 - (float(ref) / hyp))
    return bp



def bleu_score(hypothesis,reference):
    # List of n-gram(Unigram, Bigram, Trigram, Fourgram) words
    hyp_uni_list, ref_uni_list = tokens(hypothesis,reference)
    hyp_bi_list, ref_bi_list = bigram_words(hyp_uni_list,ref_uni_list)
    hyp_tri_list, ref_tri_list = trigram_words(hyp_uni_list,ref_uni_list)
    hyp_four_list, ref_four_list = fourgram_words(hyp_uni_list,ref_uni_list)
    print(hyp_four_list)

    # Counts of n-gram(Unigram, Bigram, Trigram, Fourgram) of Hypothesis
    count_unigram, count_bigram, count_trigram, count_fourgram, c_uni, c_bi, c_tri, c_four = count_hypothesis(hyp_uni_list,hyp_bi_list,hyp_tri_list,hyp_four_list)

    # Reference counts n-gram(Unigram, Bigram, Trigram, Fourgram)
    uni_ref_count = ref_match(hyp_uni_list,ref_uni_list,len(hyp_uni_list),len(ref_uni_list))
    bi_ref_count = ref_match(hyp_bi_list,ref_bi_list,len(hyp_bi_list),len(ref_bi_list))
    tri_ref_count = ref_match(hyp_tri_list,ref_tri_list,len(hyp_tri_list),len(ref_tri_list))
    four_ref_count = ref_match(hyp_four_list,ref_four_list,len(hyp_four_list),len(ref_four_list))

    # Calculating Minimum of Counts and ReferenceCounts
    min_count_unigram = min_count(count_unigram,uni_ref_count)
    min_count_bigram = min_count(count_unigram,bi_ref_count)
    min_count_trigram = min_count(count_unigram,tri_ref_count)
    min_count_fourgram = min_count(count_unigram,four_ref_count)

    # Calculating covered words of n-gram(Unigram, Bigram, Trigram, Fourgram)
    ClipCount_unigram = sum(min_count_unigram)
    ClipCount_bigram = sum(min_count_bigram)
    ClipCount_trigram = sum(min_count_trigram)
    ClipCount_fourgram = sum(min_count_fourgram)

    # BLEU score of n-gram(Unigram, Bigram, Trigram, Fourgram)
    try:
        Unigram_Precision = round((ClipCount_unigram / c_uni), 4)
        Bigram_Precision = round((ClipCount_bigram / c_bi), 4)
        Trigram_Precision = round((ClipCount_trigram / c_tri), 4)
        Fourgram_Precision = round((ClipCount_fourgram/c_four),4)
    except ZeroDivisionError:
        Unigram_Precision = 0
        Bigram_Precision = 0
        Trigram_Precision = 0
        Fourgram_Precision = 0
    bravity_penality = bp(len(hyp_uni_list),len(ref_uni_list))
    Geometric_mean = round((geometric_mean([Unigram_Precision,Bigram_Precision,Trigram_Precision,Fourgram_Precision])),4)
    Bleu_score= (Geometric_mean * bravity_penality)
    print("BP =",bravity_penality)
    print("Geometric Mean =", Geometric_mean)

    #print(Geometric_mean)

    if Bleu_score > 1 or Bleu_score == 1:
        Bleu_score = Bleu_score/10
    elif Bleu_score > 10 or Bleu_score == 10:
        Bleu_score = Bleu_score / 100
    elif Bleu_score > 100 or Bleu_score == 100:
        Bleu_score = Bleu_score / 1000
    print("Bleu Score =",Bleu_score)
    return Bleu_score

#print(bleu_score(Output,Reference))

