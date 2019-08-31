from django.shortcuts import render, get_object_or_404
from .models import Questions, Versions,VersionToQuestion,Entries,Answers,JotFormIDs
from user.models import Products,Scores
import requests
from datetime import date
from .forms import JotFormIDForm

#API KEY for the corresponding JotForm account
JFAPI_KEY = '7746a94a4b70e6826b90564723ec8049'

#Principle List
#This page generates the URL of the form with the corresponding principle
def principle_list(request,principle_id,product_id):
    request.session['product_id'] = product_id 
    product = get_object_or_404(Products,pk = product_id).__dict__
    oneToTen = range(1,11)

    #Get the form ID and the most recent entry
    form_ID = JotFormIDs.objects.get(principle = principle_id).jotform_id
    entries = Entries.objects.filter(product_id_id = product_id,principle = principle_id).order_by('-entry_time')

    #The base URL for the form
    url = 'https://form.jotformeu.com/jsform/' + form_ID + '?product_id=' + str(product_id)+'&username=' + str(request.user)
    if entries.count() != 0: #If there are previous entries
        entry_id = entries[0].id 
        previousAnswers = Answers.objects.filter(entry_id_id = entry_id)
        #Add the previous answers to the end of the URL to prepopulate the form
        for answer in previousAnswers:
            url += '&question_id_'+str(answer.question_id.id) + '=' + answer.answers
    

    args = {'url':url, 
            'productInfo':product,
            'oneToTen':oneToTen,
            'product_id':product_id}
    
    return render(request, 'embeded_form.html', args)


#This page is loaded as the Thank you page of each principle form
#This page loads the latest submission and store the answers
def form_completed(request, principle_id):
    product_id = request.session['product_id']
    product = get_object_or_404(Products,pk = product_id).__dict__
    form_ID = JotFormIDs.objects.get(principle = principle_id).jotform_id

    #Get the latest submissions from the corresponding form
    r = requests.get('https://eu-api.jotform.com/form/'+ form_ID +'/submissions?apiKey='+ JFAPI_KEY +'&orderby=created_at').json()['content']
    saveAnswer = []
    subFound = False
    rightSubmission = None
    oneToTen = range(1,11)
    args = {'productInfo':product,
            'oneToTen':oneToTen,
            'product_id':product_id}
    #Go through all the submissions
    for submission in r:
        #Check the fileds in each submission, until we find the one with the same username with the user
        for field in submission['answers'].values():
            if field['name'].lower().startswith('username') and field['answer'] == str(request.user):
                subFound = True
                rightSubmission = submission
                submissionID = submission['id']
                createdAt = submission['created_at']
                break
        if subFound == True:
            break

    #Debug message of there is no new submission from this user
    if not rightSubmission:
        args['message'] = 'No new submission'
        return render(request, 'form_completed.html', args)

    #Go through this submission's fields 
    for field in rightSubmission['answers'].values():
        #Fieldname starts with 'question_id_' is question fileds
        if field['name'].lower().startswith('question_id'):
            qpk = int(field['name'][12:])
            try:
                answer = field['answer']
            except:
                #Store an empty string if the anwser is empty, or it would store 'None'
                answer = ''

            #Append a list of qid and answer for later storing    
            saveAnswer.append([qpk,answer])

        #Store the version number and product_id
        elif field['name'].lower().startswith('version'):
            version = int(field['text'])
        elif field['name'].lower().startswith('product_id'):
            product_id = int(field['answer'])

    #Check if the entry already exists
    try:
        newEntry = Entries.objects.get(product_id_id = product_id, entry_time = createdAt+"-05:00")
        args['message'] = 'No new submission'
        return render(request,'form_completed.html', args)

    #Counting the number of questions answered and the total number of questions to calculate the completeness percentage
    #And then save the answers
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


#Admin function, storing JotFormIDs
def JotFormID(request):
    if request.method == 'POST':
        form = JotFormIDForm(request.POST)
        if form.is_valid():
            #Save the IDs
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
        #Prepopulate the form with current IDs
        formIDDict = {}
        for i in range(1,11):
            try:
                formIDDict['principle_'+str(i)] = JotFormIDs.objects.get(principle = i).jotform_id
            except:
                pass
        form = JotFormIDForm(formIDDict)
        message = ''

    return render(request, 'JotFormID.html', {'form': form, 'message':message})


#Admin function
#Check if the form changed
def form_changed(request):
    if request.method =='POST':
        form_IDs = JotFormIDs.objects.all()
        message=[]
        currentPrinciple = 0
        questionIDInThisVersion = []
        changeFormVersion =[]
        #Get a list of questions form the previous version
        try:
            previousVersionID = Versions.objects.latest('id').id
            questionIDInPreviousVersion = list(VersionToQuestion.objects.filter(version_id_id = previousVersionID).values_list('question_id_id',flat=True))
        except:
            #Empty list if this is the very first version
            questionIDInPreviousVersion = []
        
        #A dict of kewwords which are not questions. To identy the question fields from the other.
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
                        #Check if the question already exists
                        newQuestion = Questions.objects.get(description = content['text'])
                        message.append('success')
                    except:
                        #or create a new question
                        newQuestion = Questions(description = content['text'], in_principle = currentPrinciple)
                        newQuestion.save() #Changes

                    #Change the field_id of the questions through the JotForm API
                    requests.post('https://eu-api.jotform.com/form/'+ID.jotform_id+'/question/'+content['qid']+'?apiKey='+JFAPI_KEY,
                                       data = {'question[name]' : 'question_id_'+ str(newQuestion.pk)}) 

                    message.append(newQuestion.pk)
                    questionIDInThisVersion.append(newQuestion.pk)

                elif content['name'].lower().startswith('version'):
                    #save the filed id for the version field for later, when posting back the new version id through the API 
                    changeFormVersion.append([ID.jotform_id,content['qid']])

        questionIDInPreviousVersion.sort()
        questionIDInThisVersion.sort()
        message.append(questionIDInPreviousVersion)
        message.append(questionIDInThisVersion)

        #Check if the previous version and the current version have the same questions
        if set(questionIDInPreviousVersion) != set(questionIDInThisVersion): #Changes
            #Create a new version and store the corresponding question id in VersionToQuestion
            newVersion = Versions(online_date = date.today())
            newVersion.save()
            for qid in questionIDInThisVersion:
                try:
                    VersionToQuestion(version_id_id = newVersion.pk,question_id_id = qid).save()
                except:
                    pass
            success = 'form changed'

            for ID,qid in changeFormVersion:
                #Change the version ID on each form
                requests.post('https://eu-api.jotform.com/form/'+ID+'/question/'+str(qid)+'?apiKey='+JFAPI_KEY,
                                       data = {'question[text]' : str(newVersion.pk) })
                message.append([ID,qid])
        else:
            success = 'form not changed'
        
        return render(request,'form_changed.html',{'message':message, 'success':success})

    return render(request,'form_changed.html')


#View Previous Submissions
def view_submissions(request,entry_id,product_id):
    #Get the list of submissions
    request.session['product_id'] = product_id 
    product = get_object_or_404(Products,pk = product_id).__dict__
    oneToTen = range(1,11)
    entries = Entries.objects.filter(product_id_id = request.session['product_id']).order_by('-entry_time')
    #Display the entry selected
    showEntry = Answers.objects.filter(entry_id_id = entry_id)
    args = {'product_id':product_id,
            'productInfo':product,
            'oneToTen':oneToTen,
            'entries':entries , 
            'showEntry': showEntry}

    return render(request, 'view_submissions.html',args )

#Radar chart for individual product
def radar(request):
    product_id = request.session['product_id']
    product = get_object_or_404(Products,pk = product_id).__dict__
    oneToTen = range(1,11)        
    args = {'productInfo':product,
            'oneToTen':oneToTen,
            'product_id':product_id}
    return render(request, 'radar.html',args )


#Radar chart in analytics
def radar_analytics(request):
    
    return render(request, 'radar_analytics.html' )

#Completeness ranking view
def completeness_ranking(request):
    try:
        product_id = request.session['product_id']
    except:
        product_id = 0
    args = {'product_id':product_id}
    return render(request, 'completeness_ranking.html',args)

#Number of products ranking view
def number_ranking(request):
    return render(request, 'number_ranking.html')


#Analytics page view
def analytics(request):
    return render(request, 'analytics.html')
    
