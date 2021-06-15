import nltk,math
import difflib


#Output = open("C:\\Users\\91742\\Desktop\\Output(1 Sent).txt", encoding="utf8").read()
#Reference = open("C:\\Users\\91742\\Desktop\\Reference(1 Sent).txt", encoding="utf8").read()

#hyp = nltk.word_tokenize(Output)
#ref = nltk.word_tokenize(Reference)

#print("Hyp",hyp)
#print("Ref",ref)

# calculating continuous matching words
s = []
matches = []


def calculate_gtm(hyp,ref):
    i=0
    j=0

    for h in range(i,len(hyp)-1):
        for r in range(j,len(ref)-1):
            if hyp[h] == ref[r]:
                #print("match", hyp[h],h,ref[r],r)
                s.append(hyp[h])
                #print(s)
                j = r + 1
                #print("j",j)
                #print("h,r",h,r)
                break
            elif hyp[h] != ref[r] and len(s)>0:
                #print("not match", hyp[h],ref[r])
                matches.append(list(s))
                s.clear()
                j=j+1
                #print("else h,r",h,r)
    sum = 0
    for m in matches:
        sum = sum + len(m) ** 2
    size = float(round(math.sqrt(sum), 4))
    print("Size",size)
    print("length ",len(hyp), len(ref))
    try:
        precision = (float)(size) /(float)(len(hyp))
        recall = (float)(size) / (float)(len(ref))
    except:
        precision = 0
        recall = 0
    print("precision =",precision)
    print("recall= ",recall)
    denominator = round((precision + recall), 4)


    try:
        F_mean = (2 * (precision * recall)) / denominator
    except:
        print("An exception occurred")
        F_mean = 0
    if F_mean >1 or F_mean == 1:
        F_mean = F_mean/10
    elif F_mean > 10 or F_mean == 10:
        F_mean = F_mean / 100
    elif F_mean > 100 or F_mean == 100:
        F_mean = F_mean / 1000
    return round(F_mean, 4)


#print(calculate_gtm(hyp,ref))