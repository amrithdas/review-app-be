from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from utils.decorators import custom_auto_schema
from .models import Review

@api_view(['POST'])
@custom_auto_schema(
    operation_description="create a review",
    responses={201: 'Created'}
)
@csrf_exempt
def create_review(request):
    if request.method == 'POST':
        # Parse JSON data from request body
        data = json.loads(request.body)
        
        # Extract data fields
        name = data.get('restaurant_name')
        user_name = data.get('user_name')
        comment = data.get('comment')
        type = data.get('type')
        individual_rating = data.get('individual_rating')

        # Create new Review instance
        review = Review.objects.create(
            name=name,
            user_name=user_name,
            comment=comment,
            type=type,
            individual_rating=individual_rating
        )

        # Return success response
        return JsonResponse({'message': 'Review created successfully'}, status=201)
    else:
        # Return error response for non-POST requests
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@api_view(['GET'])
@custom_auto_schema(
    operation_description="get all reviews",
    responses={200: 'OK'}
)
def get_reviews(request):
    if request.method == 'GET':
        # Query the database to retrieve review data
        reviews = Review.objects.all()

        # Serialize review data into JSON format
        review_data = [
            {
                'name': review.name,
                'user_name': review.user_name,
                'comment': review.comment,
                'type':review.type,
                'individual_rating': review.individual_rating,
            }
            for review in reviews
        ]

        # Return JSON response containing review data
        return JsonResponse({'reviews': review_data}, status=200)
    else:
        # Return error response for non-GET requests
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
