import encodings.utf_8

import nltk
from django.shortcuts import render, HttpResponse
from home.models import Text,Results
from home.bleu import *
from home.nist import *
from home.ter import *
from home.meteor import *
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from home.gtm import *
import xlwt
from xlwt import Workbook

def main(request):
    if request.method == "POST":
        h = request.FILES.get('hypothesis')
        r = request.FILES.get('reference')
        obj = Text.objects.create(hyp=h, ref=r)
        obj.save()
        Output_file = open(obj.hyp.path, encoding="utf8").readlines()
        Reference_file = open(obj.ref.path, encoding="utf8").readlines()



        hypothesis = []
        reference = []


        hypothesis.append(str(Output_file))
        reference.append(str(Reference_file))
        print("Hypothesis =", hypothesis)
        print("Reference=", reference)



        Output = open(obj.hyp.path, encoding="utf8").read()
        Reference = open(obj.ref.path, encoding="utf8").read()
        hyp = nltk.word_tokenize(Output)
        ref = nltk.word_tokenize(Reference)
        print(hyp,len(hyp))
        print(ref,len(hyp))

        t = ter_score(ref,hyp)
        n = calculate_nist(ref,hyp)
        b = bleu_score(hypothesis,reference)
        m = meteor_score(hyp,ref)
        g = calculate_gtm(hyp,ref)

        print("ter ",t)
        print("nist",n)
        print("bleu",b )
        print("meteor",m )
        print("gtm",g )

        # Scores per sentences
        t_scores=[]
        b_scores=[]
        n_scores=[]
        m_scores=[]
        g_scores=[]
        hypo=[]
        refs=[]
        for i in range(0,len(Output_file)):
            hyp_tokens = nltk.word_tokenize(Output_file[i])
            ref_tokens = nltk.word_tokenize(Reference_file[i])
            t_scores.append(ter_score(ref_tokens,hyp_tokens))
            hypo.append(str(Output_file[i]))
            refs.append(str(Reference_file[i]))
            b_scores.append(bleu_score(hypo, refs))
            n_scores.append(calculate_nist(ref_tokens,hyp_tokens))
            m_scores.append(meteor_score(hyp_tokens,ref_tokens))
            g_scores.append(calculate_gtm(hyp_tokens,ref_tokens))
        print(t_scores)
        print(b_scores)
        print(m_scores)
        print(n_scores)
        print(g_scores)

        # creating excel sheet of scores per sentences
        wb = Workbook()

        # add_sheet is used to create sheet.
        sheet1 = wb.add_sheet('Sheet 1')
        style = xlwt.easyxf('align: wrap yes')
        bold = xlwt.easyxf('font: Bold on ; align: wrap on')

        sheet1.write(0, 0, 'OUTPUT SENTENCES', bold)
        for i in range(0, len(Output_file)):
            sheet1.write(i+1, 0, Output_file[i], style)

        sheet1.write(0, 1, 'REFERENCE SENTENCES', bold)
        for i in range(0, len(Reference_file)):
            sheet1.write(i+1, 1, Reference_file[i], style)

        sheet1.write(0, 2, 'TER', bold)
        for i in range(0, len(t_scores)):
            sheet1.write(i+1, 2, t_scores[i], style)

        sheet1.write(0, 3, 'BLEU', bold)
        for i in range(0, len(b_scores)):
            sheet1.write(i+1, 3, b_scores[i], style)

        sheet1.write(0, 4, 'NIST', bold)
        for i in range(0, len(n_scores)):
            sheet1.write(i+1, 4, n_scores[i], style)

        sheet1.write(0, 5, 'METEOR', bold)
        for i in range(0, len(m_scores)):
            sheet1.write(i+1, 5, m_scores[i], style)

        sheet1.write(0, 6, 'GTM', bold)
        for i in range(1, len(g_scores)):
            sheet1.write(i, 6, g_scores[i], style)

        wb.save('evaluate/static/evaluate/Scores list.xls')

        # graph

        # create data
        x = ['GTM', 'TER', 'Meteor', 'Bleu','Nist']
        y = [g, t, m, b, n]  # score
        x_pos = np.arange(len(x))

        fig, ax = plt.subplots()

        # Add title and axis names
        plt.xlabel(' Evaluation ')
        plt.ylabel(' scores ')
        plt.title('graph')

        # Create bars and choose color

        plt.bar(x[0], y[0], color='grey', width=0.3)
        plt.bar(x[1], y[1], color='pink', width=0.3)
        plt.bar(x[2], y[2], color='yellow', width=0.3)
        plt.bar(x[3], y[3], color='red', width=0.3)
        plt.bar(x[4], y[4], color ='green', width=0.3)

        # Create names on the x axis
        plt.xticks(x_pos, x)
        plt.savefig('evaluate/static/evaluate/graph.png')

        result = Results(hypothesis_file=h,reference_file=r,graph='evaluate/static/evaluate/graph.png',
                         scores_list='excel1.xls')
        result.save()



        return render(request, 'evaluate/scoreboard.html', {'ter': t, 'meteor': m, 'bleu': b, 'nist': n,'gtm': g})
    return render(request, 'home/home.html')









