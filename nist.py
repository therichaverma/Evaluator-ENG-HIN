import math

import nltk
from nltk import ngrams
from collections import Counter

#Output = open("C:\\Users\\91742\\Desktop\\Out.txt", encoding="utf8").read()
#Reference = open("C:\\Users\\91742\\Desktop\\Ref.txt", encoding="utf8").read()

#hyp = nltk.word_tokenize(Output)
#ref = nltk.word_tokenize(Reference)
#print(hyp)
#print(ref)


def length_penalty(lr,lh):
    ratio = lr / lh
    if 0 < ratio < 1:
        r, s = 1.5, 0.5
        beta = math.log(s) / math.log(r) ** 2
        return math.exp(beta * math.log(ratio) ** 2)
    else:
        return max(min(ratio, 1.0), 0.0)

def calculate_nist(ref,hyp):
    n_gram = Counter()
    total_ref_words = 0
    for i in range(1, 5):
        n_gram.update(ngrams(ref, i))
    total_ref_words += len(ref)

    # calculating information weights of reference ngrams
    information_weights = {}
    for n in n_gram:
        m = n[:-1]
        if m and m in n_gram:
            numerator = n_gram[m]
        else:
            numerator = total_ref_words
        information_weights[n] = math.log(numerator / n_gram[n], 2)
    print("information weights =", information_weights)
    precision_numerator = Counter()
    precision_denominator = Counter()

    # calculating ngrams where n is 1 - 4
    for i in range(1, 5):
        if len(hyp) >= i:
            hyp_ngrams = Counter(ngrams(hyp, i))
        else :
            hyp_ngrams = Counter()

        if len(ref) >= i:
            ref_ngrams = Counter(ngrams(ref, i))
        else :
            ref_ngrams = Counter()

        n_gram_common = hyp_ngrams & ref_ngrams

        # nist_precision

        numerator_ = sum(information_weights[ngram] * count for ngram, count in n_gram_common.items())
        denominator_ = sum(hyp_ngrams.values())

        if denominator_ == 0:
            p= 0
        else:
            p = numerator_/denominator_

        precision_numerator[i] += numerator_
        precision_denominator[i] += denominator_


    precision = 0
    for i in precision_numerator:
        try:
            pr = (precision_numerator[i] / precision_denominator[i])
        except ZeroDivisionError:
            pr=0
        precision += pr
    # eqn 3
    score = precision * length_penalty(len(ref),len(hyp))

    if score > 1 or score == 1:
        score = score/10
    elif score > 10 or score == 10:
        score = score / 100
    elif score > 100 or score == 100:
        score = score / 1000
    print("LP =",length_penalty(len(ref),len(hyp)))
    print("NIST =",round(score,4))
    return round(score,4)



