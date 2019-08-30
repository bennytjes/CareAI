from django.shortcuts import render, get_object_or_404
from .models import Questions, Versions,VersionToQuestion,Entries,Answers,JotFormIDs
from user.models import Products,Scores
import requests
from datetime import date
from .forms import JotFormIDForm
# Create your views here.

#API KEY for the corresponding JotForm account
JFAPI_KEY = '7746a94a4b70e6826b90564723ec8049'


def principle_list(request,principle_id,product_id):
    request.session['product_id'] = product_id 
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
    r = requests.get('https://eu-api.jotform.com/form/'+ form_ID +'/submissions?apiKey='+ JFAPI_KEY +'&orderby=created_at').json()['content']
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
        args['message'] = 'No new submission'
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
        newEntry = Entries.objects.get(product_id_id = product_id, entry_time = createdAt+"-05:00")
        args['message'] = 'No new submission'
        return render(request,'form_completed.html', args)
    except:
        qCount = 0
        aCount = 0
        newEntry = Entries(product_id_id = product_id, version_id_id = version, entry_time = createdAt+"-05:00", jotform_submission_id = submissionID, principle = principle_id )
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
            
            
    args['message'] = 'Form Submitted. Please select another form on the left.'
    return render(request,'form_completed.html', args)


def JotFormID(request):
    if request.method == 'POST':
        form = JotFormIDForm(request.POST)
        if form.is_valid():
            for i in range(1,11):
                try:
                    jfID = JotFormIDs.objects.get(principle = i)
                except:
                    jfID = JotFormIDs(principle =i)
                jfID.jotform_id = form.cleaned_data['principle_'+str(i)]
                jfID.save()

            message = "ID saved"
        else:
            message = "Invalid Form"

    else:
        formIDDict = {}
        for i in range(1,11):
            try:
                formIDDict['principle_'+str(i)] = JotFormIDs.objects.get(principle = i).jotform_id
            except:
                pass
        form = JotFormIDForm(formIDDict)
        message = ''

    return render(request, 'JotFormID.html', {'form': form, 'message':message})


def form_changed(request):
    if request.method =='POST':
        form_IDs = JotFormIDs.objects.all()
        message=[]
        currentPrinciple = 0
        questionIDInThisVersion = []
        changeFormVersion =[]
        try:
            previousVersionID = Versions.objects.latest('id').id
            questionIDInPreviousVersion = list(VersionToQuestion.objects.filter(version_id_id = previousVersionID).values_list('question_id_id',flat=True))
        except:
            questionIDInPreviousVersion = []
        

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
            r = requests.get('https://eu-api.jotform.com/form/'+ID.jotform_id+'/questions?apiKey='+JFAPI_KEY).json()['content']
            currentPrinciple = ID.principle

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

                    requests.post('https://eu-api.jotform.com/form/'+ID.jotform_id+'/question/'+content['qid']+'?apiKey='+JFAPI_KEY,
                                       data = {'question[name]' : 'question_id_'+ str(newQuestion.pk)}) #Changes

                    message.append(newQuestion.pk)
                    questionIDInThisVersion.append(newQuestion.pk)
                elif content['name'].lower().startswith('version'):
                    changeFormVersion.append([ID,content['qid']])

        questionIDInPreviousVersion.sort()
        questionIDInThisVersion.sort()
        message.append(questionIDInPreviousVersion)
        message.append(questionIDInThisVersion)

        if set(questionIDInPreviousVersion) != set(questionIDInThisVersion): #Changes
            newVersion = Versions(online_date = date.today())
            newVersion.save()
            for qid in questionIDInThisVersion:
                try:
                    VersionToQuestion(version_id_id = newVersion.pk,question_id_id = qid).save()
                except:
                    pass
            success = 'form changed'

            for ID,qid in changeFormVersion:
                requests.post('https://eu-api.jotform.com/form/'+ID+'/question/'+str(qid)+'?apiKey='+JFAPI_KEY,
                                       data = {'question[text]' : str(newVersion.pk) })
                message.append([ID,qid])
        else:
            success = 'form not changed'
        
        return render(request,'form_changed.html',{'message':message, 'success':success})

    return render(request,'form_changed.html')

def view_submissions(request,entry_id,product_id):
    request.session['product_id'] = product_id 
    product = get_object_or_404(Products,pk = product_id).__dict__
    oneToTen = range(1,11)

    

    entries = Entries.objects.filter(product_id_id = request.session['product_id']).order_by('-entry_time')
    showEntry = Answers.objects.filter(entry_id_id = entry_id)
    args = {'product_id':product_id,
            'productInfo':product,
            'oneToTen':oneToTen,
            'entries':entries , 
            'showEntry': showEntry}

    return render(request, 'view_submissions.html',args )

def radar(request):
    product_id = request.session['product_id']
    product = get_object_or_404(Products,pk = product_id).__dict__
    oneToTen = range(1,11)        
    args = {'productInfo':product,
            'oneToTen':oneToTen,
            'product_id':product_id}
    return render(request, 'radar.html',args )

def radar_analytics(request):
    
    return render(request, 'radar_analytics.html' )

def completeness_ranking(request):
    try:
        product_id = request.session['product_id']
    except:
        product_id = 0
    args = {'product_id':product_id}
    return render(request, 'completeness_ranking.html',args)

def number_ranking(request):
    return render(request, 'number_ranking.html')

def analytics(request):
    return render(request, 'analytics.html')
    
