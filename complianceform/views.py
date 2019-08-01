from django.shortcuts import render, get_object_or_404
from .models import *
import requests
from datetime import date
# Create your views here.


JFAPI_KEY = '7746a94a4b70e6826b90564723ec8049'

def get_form_url():
    return {'url':'a/a/a'}

def principle_list(request,product_id,principle_id):
    product = get_object_or_404(Products,pk = product_id).__dict__
    principleList = { 
        'principle 1' : { 'href' : 1},
        'principle 2' : { 'href' : 2},
        'principle 3' : { 'href' : 3},
        'principle 4' : { 'href' : 4},
        'principle 5' : { 'href' : 5}}
    
    form_ID = JotFormIDs.objects.get(principle = principle_id).jotform_id
    url = 'https://form.jotformeu.com/jsform/' + form_ID + '?product_id=' + str(product_id)
    
    return render(request, 'principle_list.html', {'url':url,'productInfo': product,'principleList': principleList , 'product_id':product_id})

def jot(request,product_id,principle_id):
    product = get_object_or_404(Products,pk = product_id).__dict__
    principleList = { 
        'principle 1' : { 'href' : 1},
        'principle 2' : { 'href' : 2},
        'principle 3' : { 'href' : 3},
        'principle 4' : { 'href' : 4},
        'principle 5' : { 'href' : 5}}

    form_ID = JotFormIDs.objects.get(principle = principle_id).jotform_id
    url = 'https://form.jotformeu.com/jsform/' + form_ID + '?product_id=' + str(product_id)

    return render(request, 'jotformembed.html', { 'url':url,'productInfo': product,'principleList': principleList, 'product_id':product_id }  )

def form_completed(request, product_id, principle_id):
    if request.method =='POST':
        form_ID = JotFormIDs.objects.get(principle = principle_id).jotform_id
        r = requests.get('https://api.jotform.com/form/'+ form_ID +'/submissions?apiKey='+ JFAPI_KEY +'&limit=1').json()['content'][0]
        createdAt = r['created_at']
        submissionID = r['id'] 
        saveAnswer = []
        for field in r['answers'].values():
            if field['name'].lower().startswith('question_id'):
                qpk = int(field['name'][12:])
                try:
                    answer = field['answer']
                except:
                    answer = 'None'
                saveAnswer.append([qpk,answer])
            elif field['name'].lower().startswith('version'):
                version = int(field['text'])

        try:
            newEntry = Entries.objects.get(product_id_id = product_id, entry_time = createdAt)
            message = 'No new entry'
            return render(request,'form_completed.html', {'message':message})
        except:
            newEntry = Entries(product_id_id = product_id, version_id_id = version, entry_time = createdAt, jotform_submission_id = submissionID, principle = principle_id )
            newEntry.save()

        for qpk, answer in saveAnswer:
            newAnswer = Answers(entry_id_id = newEntry.pk, question_id_id = qpk, answers = answer)
            newAnswer.save()

        message = 'Entry saved'
        return render(request,'form_completed.html', {'message':message})
    return render(request,'form_completed.html', {'message': 'press the button'})



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
                VersionToQuestion(version_id_id = newVersion.pk,question_id_id = qid).save()
            success = 'form changed'

            for ID,qid in changeFormVersion:
                requests.post('https://api.jotform.com/form/'+ID+'/question/'+str(qid)+'?apiKey='+JFAPI_KEY,
                                       data = {'question[text]' : str(newVersion.pk) })
                message.append([ID,qid])
        else:
            success = 'form not changed'
        

        return render(request,'form_changed.html',{'message':message, 'success':success})

    return render(request,'form_changed.html')