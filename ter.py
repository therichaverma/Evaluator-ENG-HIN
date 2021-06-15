#import nltk

#Output = open("C:\\Users\\91742\\Desktop\\Output(1 Sent).txt", encoding="utf8").read()
#Reference = open("C:\\Users\\91742\\Desktop\\Reference(1 Sent).txt", encoding="utf8").read()

#hyp = nltk.word_tokenize(Output)
#ref = nltk.word_tokenize(Reference)


def edit_dist(h, r, m, n):
    # Create a table to store results of sub calculations
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):
            # If hypotheses is empty insert all tokens of references
            if i == 0:
                dp[i][j] = j  # Min. operations = j
            # If reference is empty, remove all tokens of references
            elif j == 0:
                dp[i][j] = i  # Min. operations = i
            # If last tokens are same, ignore last tokens and change position
            elif h[i - 1] == r[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            # If last character are different, check all operations and find the minimum edit distance
            else:
                dp[i][j] = 1 + min(dp[i][j - 1],  # Insert
                                   dp[i - 1][j],  # Remove
                                   dp[i - 1][j - 1])  # Replace
    return dp[m][n]


def shifts(r, h, lr, lh):
    shift = {}
    matched = {}
    for i in range(0, min(lr, lh)):
        if r[i] == h[i]:
            matched.update({h[i]: i})
        if r[i] != h[i]:
            for j in range(0, lh - 1):
                if r[i] == h[j]:
                    if h[j] not in shift and h[j] not in matched:
                        # print(r[i], i, h[j], j)
                        shift.update({h[j]: j})
                        if i < j:
                            for a in range(j, i, -1):
                                h[a] = h[a - 1]
                            h[i] = r[i]
                        else:
                            for a in range(i, j):
                                h[a]
    #print("Shift = ",shift)
    #print("h= ",h)
    return len(shift), h





def ter_score(ref,hyp):
    s, hyp_s = shifts(ref, hyp, len(ref), len(hyp))
    edit = edit_dist(hyp_s, ref, len(hyp), len(ref))
    ter_score = (edit + s) / len(ref)

    if ter_score > 1 or ter_score == 1:
        ter_score = ter_score/10
    elif ter_score > 10 or ter_score == 10:
        ter_score = ter_score / 100
    elif ter_score > 100 or ter_score == 100:
        ter_score = ter_score / 1000

    return round(ter_score,4)



#print(shift(ref,hyp,len(ref),len(hyp)))