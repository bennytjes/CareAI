from django.shortcuts import render, get_object_or_404
from .models import *
from user.models import *
import requests
from datetime import date
from django.db.models import Subquery,Max 
import json
from django.http import JsonResponse 

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
    latestEntryFromUser = Entries.objects.raw(
        f'''SELECT DISTINCT ON (principle) id, product_id_id,principle , score
            FROM complianceform_entries
            WHERE complianceform_entries.product_id_id = {product_id}
            ORDER BY complianceform_entries.principle, entry_time DESC''')
    userScore = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0}
    pCount = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0}
    pScore = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0}
    allScore = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0}
    for entry in latestEntryFromUser:
        userScore[str(entry.principle)] = entry.score

    latestEntryFromAll = Entries.objects.raw(
        f'''SELECT DISTINCT ON (principle,product_id_id) id, product_id_id,principle , score
            FROM complianceform_entries
            ORDER BY complianceform_entries.principle, complianceform_entries.product_id_id, entry_time DESC''')
    
    for entry in latestEntryFromAll: 
        pCount[str(entry.principle)] += 1
        pScore[str(entry.principle)] += entry.score

    for p in pScore:
        try:
            allScore[p] = pScore[p]/pCount[p]
        except:
            allScore[p] = 0

    return render(request, 'radar.html', {'user':userScore ,'all': allScore})

def ranking(request):
    return render(request, 'chart_example_from_d3-graph-gallery.html',)

def returnJSON(request):
    latestEntryFromAll = Entries.objects.raw(
        f'''SELECT DISTINCT ON (principle,product_id_id) id, product_id_id,principle , score
            FROM complianceform_entries
            ORDER BY complianceform_entries.principle, complianceform_entries.product_id_id, entry_time DESC''')
    
    
    return JsonResponse(somedict,safe=False)