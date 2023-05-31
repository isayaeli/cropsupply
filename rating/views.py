from django.http import HttpResponse
import json
from django.shortcuts import render
from rating.models import Product_Rating

# Create your views here.
def product_reviews(request):
    product_id = request.POST['product_id']
    rating_value = request.POST['rating_value']
    comment = request.POST['comment']
    user = request.user

    response_data = {}
    product = Product_Rating(rating_by=user, rating_for_id=product_id, comments=comment, rating_value=rating_value, )
    product.save()

    rating = Product_Rating.objects.filter(rating_for=product_id)
    sum_of_user_rates =  sum(rating.values_list('rating_value', flat=True)) # --> rating for one user filtered above

    all_ratings_to_talent = rating.count()  * 5 # --> getting number of all ratings for a filtered user
    try:
       rates= round(sum_of_user_rates * 5 / all_ratings_to_talent, 1)
    except ZeroDivisionError:
        rates = 0
    response_data['success'] = 'Succesful submitted'
    response_data['rating_avg'] = rates
    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json'
    )