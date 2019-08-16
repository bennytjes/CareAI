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


def getRankingScores(request,group,audited):
    groupFilter = '' if group == 'All' else 'AND p.category = \'' + group+'\''
    auditedFilter = 'AND P.audited = TRUE' if audited=='true' else ''
    cursor = connection.cursor()
    cursor.execute(f'''SELECT * , (s.principle_1+s.principle_2+s.principle_3+s.principle_4+s.principle_5+s.principle_6+s.principle_7+s.principle_8+s.principle_9+s.principle_10) AS total
                      From user_scores AS s, user_products AS p
                      WHERE s.product_id_id = p.product_id {groupFilter} {auditedFilter}
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


def getProductScores(request,group,audited):

    groupFilter = '' if group == 'All' else 'AND p.category = \'' + group+'\''

    scoreList = []
    try:
        product_id = request.session['product_id']
    except:
        product_id = 1 #any product

    productScores = model_to_dict(Scores.objects.get(product_id_id = product_id))
    if group == 'False':
        groupFilter = Products.objects.get(pk = product_id).__dict__['category']
    else: 
        groupFilter = group
    

    allScores = Scores.objects.aggregate(Avg('principle_1'),Avg('principle_2'),Avg('principle_3'),Avg('principle_4'),Avg('principle_5'),Avg('principle_6'),Avg('principle_7'),Avg('principle_8'),Avg('principle_9'),Avg('principle_10'))
    groupScores = Scores.objects.filter(pk__in = Products.objects.filter(category = groupFilter).values_list('pk', flat = True)).aggregate(Avg('principle_1'),Avg('principle_2'),Avg('principle_3'),Avg('principle_4'),Avg('principle_5'),Avg('principle_6'),Avg('principle_7'),Avg('principle_8'),Avg('principle_9'),Avg('principle_10'))


    
    scoreList = [productScores,allScores,groupScores]
    return JsonResponse(scoreList,safe = False)

def getNumberRanking(request,group,audited):
    groupFilter = '' if group == 'All' else 'AND p.category = \'' + group+'\''
    auditedFilter = 'AND P.audited = TRUE' if audited=='true' else ''
    cursor = connection.cursor()
    cursor.execute(f'''SELECT organisation, COUNT(p.product_id) AS product_count
                      FROM user_userdetails AS d, user_products AS p
                      WHERE d.user_id = p.user_id {groupFilter} {auditedFilter}
                      GROUP BY organisation 
                      ORDER BY product_count DESC
                      LIMIT 10''')

    productCounts = dictfetchall(cursor)
    return JsonResponse(productCounts,safe=False)

def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

