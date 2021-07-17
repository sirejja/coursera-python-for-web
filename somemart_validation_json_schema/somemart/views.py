  
import json

from django import forms
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator

from .models import Item, Review


from jsonschema import validate
from jsonschema.exceptions import ValidationError

REVIEW_SCHEMA_AddItemView = {
	"$schema": "https://json-schema.org/draft/2019-09/schema",
    'type':'object',
    'properties':{
            'title':{
              'type':'string',
              'minLength': 1,
              'maxLength': 64,
            },
              'description':{
              'type':'string',
              'minLength': 1,
              'maxLength': 1024,
            },
              'price':{
              'type':'integer',
              'minimum': 1,
              'maximum': 100,
            },
     },
     'required':['title', 'description','price'],      
}


REVIEW_SCHEMA_PostReviewView = {
	"$schema": "https://json-schema.org/draft/2019-09/schema",
    'type':'object',
    'properties':{
            'text':{
              'type':'string',
              'minLength': 1,
              'maxLength': 1024,
            },
              'grade':{
              'type':'integer',
              'minimum': 1,
              'maximum': 10,
            },
     },
     'required':['text','grade'],      
}


class GoodForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=1024)
    price = forms.IntegerField(min_value=1, max_value=1000000)


class ReviewForm(forms.Form):
    text = forms.CharField(min_length=1, max_length=1024)
    grade = forms.IntegerField(min_value=1, max_value=10)


class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            document = json.loads(request.body)
            validate(document, REVIEW_SCHEMA_AddItemView)
            item = Item(title=document['title'], description=document['description'], price=document['price'])
            item.save()
            data = {'id': item.pk}
            return JsonResponse(data, status=201)
        except json.JSONDecodeError:
            return HttpResponse(status=400)
        except ValidationError:
            return HttpResponse(status=400)
            
        
@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        data = {'id': item_id}
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse(status=404, data={})
        try:
            document = json.loads(request.body)
            validate(document, REVIEW_SCHEMA_PostReviewView)
            review = Review(text=document['text'], grade=document['grade'], item=item)
            review.save()
            return JsonResponse({'id': review.id}, status=201)
        except json.JSONDecodeError:
            return HttpResponse(status=400)
        except ValidationError:
            return HttpResponse(status=400)

      
class GetItemView(View):
    """View для получения информации о товаре.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.prefetch_related('review_set').get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse(status=404, data={})
        item_dict = model_to_dict(item)
        item_reviews = [model_to_dict(x) for x in item.review_set.all()]
        item_reviews = sorted(
            item_reviews, key=lambda review: review['id'], reverse=True)[:5]
        for review in item_reviews:
            review.pop('item', None)
        item_dict['reviews'] = item_reviews
        return JsonResponse(item_dict, status=200)