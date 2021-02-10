from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from EthicAssessmentSoftware.models import *
from EthicAssessmentSoftware.serializers import *

# Create your views here.
# source: https://bezkoder.com/django-crud-mysql-rest-framework/#:~:text=First%2C%20we%20setup%20Django%20Project,operations%20(including%20custom%20finder).
# TODO: potentially include forms from https://www.laravelcode.com/post/django-3-crud-tutorial-example-with-mysql-and-bootstrap

# endpoint for Anwendung
@api_view(['GET','POST','DELETE'])
def anwendung_list(request):
    # GET for Anwendung
    if request.method == 'GET':
        anwendungen = Anwendung.objects.all()
        anwendungen_serializer = AnwendungSerializer(anwendungen, many=True)
        return JsonResponse(anwendungen_serializer.data, safe=False)

    # POST for Anwendung
    elif request.method == 'POST':
        anwendung_data = JSONParser().parse(request)
        anwendung_serializer = AnwendungSerializer(data=anwendung_data)
        if anwendung_serializer.is_valid():
            anwendung_serializer.save()
            # Theoretically one could respond with the data sent. We don't do so here because of reflection attacks
            return JsonResponse({},status=status.HTTP_201_CREATED)
        else:
            # This should NOT return the errors to not reveal internal server errors. Instead this SHOULD be logged. But this is the insecure first version.
            return JsonResponse(AnwendungSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE for Anwendung
    elif request.method == 'DELETE':
        counter = Anwendung.objects.all().delete()
        return JsonResponse({'message': '{} Anwendungen were deleted successfully!'.format(counter[0])}, status=status.HTTP_200_OK)

    # block for any other methods. This should be blocked by the api_view spec, but as a doc / security measure:
    else:
        return JsonResponse('',status=status.HTTP_405_METHOD_NOT_ALLOWED)

# endpoint for Anwendung details
@api_view(['GET', 'PUT', 'DELETE'])
def anwendung_details(request, anwendung_name):
    # I assume this to work via 'name'. Potentially some more DB-specific field name is requried, most docs use pk
    try:
        anwendung = Anwendung.objects.get(pk=anwendung_name)
    except Anwendung.DoesNotExist:
        return JsonResponse({'message': 'the requested object does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # GET for Anwendung with condition
    if request.method == 'GET':
        anwendung_serializer = AnwendungSerializer(anwendung)
        return JsonResponse(anwendung_serializer.data, status=status.HTTP_200_OK)

    # PUT for Anwendung
    elif request.method == 'PUT':
        anwendung_data = JSONParser.parse(request)
        anwendung_serializer = AnwendungSerializer(anwendung, data=anwendung_data)
        if anwendung_serializer.is_valid():
            anwendung_serializer.save()
            # Theoretically one could respond with the data sent. We don't do so here because of reflection attacks
            return JsonResponse({}, status=status.HTTP_201_CREATED)
        else:
            # This should NOT return the errors to not reveal internal server errors. Instead this SHOULD be logged. But this is the insecure first version.
            return JsonResponse(AnwendungSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE for Anwendung with conditions
    elif request.method == 'DELETE':
        anwendung.delete()
        return JsonResponse({'message': 'Anwendungen was deleted successfully!'}, status=status.HTTP_200_OK)

    # block for any other methods. This should be blocked by the api_view spec, but as a doc / security measure:
    else:
        return JsonResponse('', status=status.HTTP_405_METHOD_NOT_ALLOWED)

# endpoint for Stakeholder
@api_view(['GET','POST','DELETE'])
def anwendung_stakeholder_list(request, anwendung_name):
    # I assume this to work via 'name'. Potentially some more DB-specific field name is requried, most docs use pk
    # This is only done here to catch cases where the declared Anwendung does not exist
    try:
        anwendung_object = Anwendung.objects.get(pk=anwendung_name)
    except Anwendung.DoesNotExist:
        return JsonResponse({'message': 'the requested object does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # GET for Stakeholder
    if request.method == 'GET':
        # get Stakeholder via "Find all objects by condition"
        stakeholders = Stakeholder.objects.filter(pk = anwendung_name)
        stakeholder_serializer = StakeholderSerializer(stakeholders, many=True)
        return JsonResponse(StakeholderSerializer.data, status=status.HTTP_200_OK, safe=False)

    # POST for Stakeholder
    # TODO: Potentially, anwendung_name should be used as part of this as well to be inserted before serialization
    # For that, see https://sunscrapers.com/blog/the-ultimate-tutorial-for-django-rest-framework-functional-endpoints-and-api-nesting-part-6/
    if request.method == 'POST':
        stakeholder_data = JSONParser().parse(request)
        stakeholder_serializer = StakeholderSerializer(data=stakeholder_data)
        if stakeholder_serializer.is_valid():
            stakeholder_serializer.save()
            return JsonResponse({},status=status.HTTP_201_CREATED)

    # Delete for Stakeholders with condition
    if request.method == 'DELETE':
        # get Stakeholder via "Find all objects by condition"
        Stakeholder.objects.filter(anwendung=anwendung_name).delete()
        return JsonResponse({'message':'objects deleted'}, status=status.HTTP_200_OK)
