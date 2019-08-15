from django.shortcuts import render, get_object_or_404
from .models import *
from user.models import *
import requests
from datetime import date
from django.db.models import Subquery,Max ,Avg
import json
from django.http import JsonResponse 
from django.forms.models import model_to_dict
from django.core.serializers import serialize
from django.db import connection
from django.utils.safestring import SafeString

# Create your views here.


JFAPI_KEY = '7746a94a4b70e6826b90564723ec8049'


def principle_list(request,principle_id):
    product_id = request.session['product_id']
    product = get_object_or_404(Products,pk = product_id).__dict__
    oneToTen = range(1,11)
    form_ID = JotFormIDs.objects.get(principle = principle_id).jotform_id

    entries = Entries.objects.filter(product_id_id = product_id,principle = principle_id).order_by('-entry_time')
    url = 'https://form.jotformeu.com/jsform/' + form_ID + '?product_id=' + str(product_id)+'&username=' + str(request.user)
    if entries.count() != 0: #no previous entry
        entry_id = entries[0].id 
        previousAnswers = Answers.objects.filter(entry_id_id = entry_id)
        for answer in previousAnswers:
            url += '&question_id_'+str(answer.question_id.id) + '=' + answer.answers
    

    args = {'url':url, 
            'productInfo':product,
            'oneToTen':oneToTen,
            'product_id':product_id}
    
    return render(request, 'embeded_form.html', args)


def form_completed(request, principle_id):
    product_id = request.session['product_id']
    product = get_object_or_404(Products,pk = product_id).__dict__
    form_ID = JotFormIDs.objects.get(principle = principle_id).jotform_id
    r = requests.get('https://api.jotform.com/form/'+ form_ID +'/submissions?apiKey='+ JFAPI_KEY +'&orderby=created_at').json()['content']
    saveAnswer = []
    subFound = False
    rightSubmission = None
    oneToTen = range(1,11)
    args = {'productInfo':product,
            'oneToTen':oneToTen,
            'product_id':product_id}

    for submission in r:
        for field in submission['answers'].values():
            if field['name'].lower().startswith('username') and field['answer'] == str(request.user):
                subFound = True
                rightSubmission = submission
                submissionID = submission['id']
                createdAt = submission['created_at']
                break
        if subFound == True:
            break

    if not rightSubmission:
        args['message'] = 'no new sub'
        return render(request, 'form_completed.html', args)

    for field in rightSubmission['answers'].values():
        if field['name'].lower().startswith('question_id'):
            qpk = int(field['name'][12:])
            try:
                answer = field['answer']
            except:
                answer = ''
            saveAnswer.append([qpk,answer])
        elif field['name'].lower().startswith('version'):
            version = int(field['text'])
        elif field['name'].lower().startswith('product_id'):
            product_id = int(field['answer'])

    try:
        newEntry = Entries.objects.get(product_id_id = product_id, entry_time = createdAt)
        args['message'] = 'No new entry'
        return render(request,'form_completed.html', args)
    except:
        qCount = 0
        aCount = 0
        newEntry = Entries(product_id_id = product_id, version_id_id = version, entry_time = createdAt, jotform_submission_id = submissionID, principle = principle_id )
        newEntry.save()
        for qpk, answer in saveAnswer:
            qCount +=1
            if answer != '': aCount +=1 
            newAnswer = Answers(entry_id_id = newEntry.pk, question_id_id = qpk, answers = answer)
            newAnswer.save()
        newEntry.score = aCount/qCount
        newEntry.save()
        try:
            attrString = 'principle_'+ str(principle_id)
            saveScore = Scores.objects.get(product_id_id = product_id)
            setattr(saveScore, attrString , aCount/qCount)
            saveScore.save()
            
        except:
            attrString = 'principle_'+ str(principle_id)
            saveScore = Scores(product_id_id = product_id)
            setattr(saveScore, attrString , aCount/qCount)
            saveScore.save()
            
            
    args['message'] = 'Entry saved'
    return render(request,'form_completed.html', args)


    



def form_changed(request):
    if request.method =='POST':
        form_IDs = JotFormIDs.objects.values_list('jotform_id',flat=True)
        message=[]
        currentPrinciple = 0
        questionIDInThisVersion = []
        changeFormVersion =[]
        previousVersionID = Versions.objects.latest('id').id
        questionIDInPreviousVersion = list(VersionToQuestion.objects.filter(version_id_id = previousVersionID).values_list('question_id_id',flat=True))

        notQuestionNames = {
            'header': 'head',
            'header_default': 'principle',
            'submit button' : 'submit',
            'product id' : 'product',
            'version id' : 'version',
            'username': 'username'
        }
        # Itterate through the forms
        for ID in form_IDs:
            r = requests.get('https://api.jotform.com/form/'+ID+'/questions?apiKey='+JFAPI_KEY).json()['content']
            currentPrinciple += 1

            # Itterate through the items in each form response
            for content in r.values():
                message.append([currentPrinciple,content['name'],content['text'],content['qid']])

                # Only check if the name of the item starts with 'question_id_'
                # Excluding out heading, submit button, etc.
                if not content['name'].lower().startswith((tuple(notQuestionNames.values()))):
                    try:
                        newQuestion = Questions.objects.get(description = content['text'])
                        message.append('success')
                    except:
                        newQuestion = Questions(description = content['text'], in_principle = currentPrinciple)
                        newQuestion.save() #Changes

                    requests.post('https://api.jotform.com/form/'+ID+'/question/'+content['qid']+'?apiKey='+JFAPI_KEY,
                                       data = {'question[name]' : 'question_id_'+ str(newQuestion.pk)}) #Changes

                    message.append(newQuestion.pk)
                    questionIDInThisVersion.append(newQuestion.pk)
                elif content['name'].lower().startswith('version'):
                    changeFormVersion.append([ID,content['qid']])

        questionIDInPreviousVersion.sort()
        questionIDInThisVersion.sort()
        message.append(questionIDInPreviousVersion)
        message.append(questionIDInThisVersion)

        if questionIDInPreviousVersion != questionIDInThisVersion: #Changes
            newVersion = Versions(online_date = date.today())
            newVersion.save()
            for qid in questionIDInThisVersion:
                try:
                    VersionToQuestion(version_id_id = newVersion.pk,question_id_id = qid).save()
                except:
                    pass
            success = 'form changed'

            for ID,qid in changeFormVersion:
                requests.post('https://api.jotform.com/form/'+ID+'/question/'+str(qid)+'?apiKey='+JFAPI_KEY,
                                       data = {'question[text]' : str(newVersion.pk) })
                message.append([ID,qid])
        else:
            success = 'form not changed'
        

        return render(request,'form_changed.html',{'message':message, 'success':success})

    return render(request,'form_changed.html')

def view_submissions(request,entry_id):
    entries = Entries.objects.filter(product_id_id = request.session['product_id']).order_by('-entry_time')
    showEntry = Answers.objects.filter(entry_id_id = entry_id)
    return render(request, 'view_submissions.html', {'entries':entries , 'showEntry': showEntry})

def radar(request):
    product_id = request.session['product_id']
    product = get_object_or_404(Products,pk = product_id).__dict__
    oneToTen = range(1,11)        
    args = {'productInfo':product,
            'oneToTen':oneToTen,
            'product_id':product_id}
    return render(request, 'radar.html',args )


def getProductScores(request):
    scoreList = []
    product_id = request.session['product_id']
    productScores = model_to_dict(Scores.objects.get(product_id_id = product_id))
    allScores = Scores.objects.aggregate(Avg('principle_1'),Avg('principle_2'),Avg('principle_3'),Avg('principle_4'),Avg('principle_5'),Avg('principle_6'),Avg('principle_7'),Avg('principle_8'),Avg('principle_9'),Avg('principle_10'))
    groupScores = Scores.objects.filter(pk__in = Products.objects.filter(category = Products.objects.get(pk = product_id).__dict__['category']).values_list('pk', flat = True)).aggregate(Avg('principle_1'),Avg('principle_2'),Avg('principle_3'),Avg('principle_4'),Avg('principle_5'),Avg('principle_6'),Avg('principle_7'),Avg('principle_8'),Avg('principle_9'),Avg('principle_10'))
    
    
    scoreList = [productScores,allScores,groupScores]
   

    return JsonResponse(scoreList,safe = False)



def completeness_ranking(request):
    try:
        product_id = request.session['product_id']
    except:
        product_id = 0
    args = {'product_id':product_id}
    return render(request, 'completeness_ranking.html',args)

def number_ranking(request):
    cursor = connection.cursor()
    cursor.execute('''SELECT organisation, COUNT(p.product_id) AS product_count
                      FROM user_userdetails AS d, user_products AS p
                      WHERE d.user_id = p.user_id
                      GROUP BY organisation 
                      ORDER BY product_count DESC
                      LIMIT 10''')
    productCounts = dictfetchall(cursor)
    productCountsJSON = json.dumps(productCounts)
    return render(request, 'number_ranking.html', {'productCountsJSON':SafeString(productCountsJSON),'productCounts':productCounts})

def rankingScore(request,group):
    groupFilter = '' if group == 'All' else 'AND p.category = \'' + group+'\''
    cursor = connection.cursor()
    cursor.execute(f'''SELECT * , (s.principle_1+s.principle_2+s.principle_3+s.principle_4+s.principle_5+s.principle_6+s.principle_7+s.principle_8+s.principle_9+s.principle_10) AS total
                      From user_scores AS s, user_products AS p
                      WHERE s.product_id_id = p.product_id {groupFilter}
                      ORDER BY total DESC''')
    productScores = dictfetchall(cursor)
    scoreList =[]
    for row in productScores:
        scoreList.append({'product_name': row['product_name'],
                          'total' : row['total'],
                          'principle_1':row['principle_1'],
                          'principle_2':row['principle_2'],
                          'principle_3':row['principle_3'],
                          'principle_4':row['principle_4'],
                          'principle_5':row['principle_5'],
                          'principle_6':row['principle_6'],
                          'principle_7':row['principle_7'],
                          'principle_8':row['principle_8'],
                          'principle_9':row['principle_9'],
                          'principle_10':row['principle_10']})
    
    return JsonResponse(scoreList,safe=False)

def groupRankingScore(request):
    cursor = connection.cursor()
    cursor.execute('''SELECT * , (s.principle_1+s.principle_2+s.principle_3+s.principle_4+s.principle_5+s.principle_6+s.principle_7+s.principle_8+s.principle_9+s.principle_10) AS total
                      From user_scores AS s, user_products AS p
                      WHERE s.product_id_id = p.product_id AND p.category = 'Health promotion'
                      ORDER BY total DESC''')
    scoreList =[]
    for row in productScores:
        scoreList.append({'product_name': row['product_name'],
                          'total' : row['total'],
                          'principle_1':row['principle_1'],
                          'principle_2':row['principle_2'],
                          'principle_3':row['principle_3'],
                          'principle_4':row['principle_4'],
                          'principle_5':row['principle_5'],
                          'principle_6':row['principle_6'],
                          'principle_7':row['principle_7'],
                          'principle_8':row['principle_8'],
                          'principle_9':row['principle_9'],
                          'principle_10':row['principle_10']})
    
    return JsonResponse(scoreList,safe=False)

def analytics(request):
    return render(request, 'analytics.html')
    

def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

