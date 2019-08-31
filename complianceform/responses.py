from user.models import Scores, Products
from django.db.models import Subquery,Max ,Avg
from django.http import JsonResponse 
from django.forms.models import model_to_dict
from django.db import connection

#JSON response for the Stacked Bar Chart
def getRankingScores(request,group,audited):
    #Load the filter for the query
    groupFilter = '' if group == 'All' else 'AND p.category = \'' + group+'\''
    auditedFilter = 'AND P.audited = TRUE' if audited=='true' else ''
    cursor = connection.cursor()

    #The raw SQL query for geting the scores of top ten compliance completeness
    cursor.execute(f'''SELECT * , (s.principle_1+s.principle_2+s.principle_3+s.principle_4+s.principle_5+s.principle_6+s.principle_7+s.principle_8+s.principle_9+s.principle_10) AS total
                      From user_scores AS s, user_products AS p
                      WHERE s.product_id_id = p.product_id {groupFilter} {auditedFilter}
                      ORDER BY total DESC
                      LIMIT 10''')
    productScores = dictfetchall(cursor)
    scoreList =[]

    #Turning the result into a list of JSON
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


#JSON response for the Radar Chart
def getProductScores(request,group,audited):
    groupFilter = '' if group == 'All' else 'AND p.category = \'' + group+'\''
    scoreList = []

    try:
        product_id = request.session['product_id']
    except:
        #If not product_id stored in session, meaning tha this request is from the analytics page without clicking into any product details yet
        product_id = Scores.objects.all()[0].product_id_id #assign the product id from any product

    productScores = model_to_dict(Scores.objects.get(product_id_id = product_id))
    if group == 'False':
        groupFilter = Products.objects.get(pk = product_id).__dict__['category']
    else: 
        groupFilter = group
    
    #Get the score from all products and from the group
    allScores = Scores.objects.aggregate(Avg('principle_1'),Avg('principle_2'),Avg('principle_3'),Avg('principle_4'),Avg('principle_5'),Avg('principle_6'),Avg('principle_7'),Avg('principle_8'),Avg('principle_9'),Avg('principle_10'))
    groupScores = Scores.objects.filter(pk__in = Products.objects.filter(category = groupFilter).values_list('pk', flat = True)).aggregate(Avg('principle_1'),Avg('principle_2'),Avg('principle_3'),Avg('principle_4'),Avg('principle_5'),Avg('principle_6'),Avg('principle_7'),Avg('principle_8'),Avg('principle_9'),Avg('principle_10'))


    
    scoreList = [productScores,allScores,groupScores]
    return JsonResponse(scoreList,safe = False)

#JSON response for number of products ranking.
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

    productCounts = dictfetchall(cursor)[:10]
    return JsonResponse(productCounts,safe=False)


#Fucntion to change the raw query result to dict
#Provided by https://docs.djangoproject.com/en/2.2/topics/db/sql/
def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

