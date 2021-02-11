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

# For composition of field lookups inside get() and filter(), see
# https://docs.djangoproject.com/en/3.1/topics/db/queries/#field-lookups
# TODO: Potentially rework GET requests fro _list methods to respect 404

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
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE for Anwendung
    elif request.method == 'DELETE':
        counter = Anwendung.objects.all().delete()
        return JsonResponse({'message': '{} Anwendungen were deleted successfully!'.format(counter[0])}, status=status.HTTP_200_OK)

    # block for any other methods. This should be blocked by the api_view spec, but as a doc / security measure:
    else:
        return JsonResponse({},status=status.HTTP_405_METHOD_NOT_ALLOWED)

# endpoint for Anwendung details
@api_view(['GET', 'PUT', 'DELETE'])
def anwendung_details(request, anwendung_name):
    # I assume this to work via 'name'. Potentially some more DB-specific field name is requried, most docs use pk
    try:
        anwendung = Anwendung.objects.get(name=anwendung_name)
    except Anwendung.DoesNotExist:
        return JsonResponse({'message': 'the requested object does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # GET for Anwendung with condition
    if request.method == 'GET':
        anwendung_serializer = AnwendungSerializer(anwendung)
        return JsonResponse(anwendung_serializer.data, status=status.HTTP_200_OK)

    # PUT for Anwendung
    elif request.method == 'PUT':
        anwendung_data = JSONParser().parse(request)
        anwendung_serializer = AnwendungSerializer(anwendung, data=anwendung_data, partial=False)
        if anwendung_serializer.is_valid():
            # This needs to be added to remove the old Anwendung. You can only change the name via PUT here, which is the primary key.
            # So if you exec this without the following delete call, a new Anwendung will simply be created. Which is not the intention of PUT here.
            anwendung.delete()
            anwendung_serializer.save()
            # Theoretically one could respond with the data sent. We don't do so here because of reflection attacks
            return JsonResponse({}, status=status.HTTP_202_ACCEPTED)
        else:
            # This should NOT return the errors to not reveal internal server errors. Instead this SHOULD be logged. But this is the insecure first version.
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE for Anwendung with conditions
    elif request.method == 'DELETE':
        anwendung.delete()
        return JsonResponse({'message': 'Anwendungen was deleted successfully!'}, status=status.HTTP_200_OK)

    # block for any other methods. This should be blocked by the api_view spec, but as a doc / security measure:
    else:
        return JsonResponse({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# endpoint for Stakeholder
@api_view(['GET','POST','DELETE'])
def anwendung_stakeholder_list(request, anwendung_name):
    # I assume this to work via 'name'. Potentially some more DB-specific field name is requried, most docs use pk
    # This is only done here to catch cases where the declared Anwendung does not exist
    try:
        anwendung_object = Anwendung.objects.get(name=anwendung_name)
    except Anwendung.DoesNotExist:
        return JsonResponse({'message': 'no stakeholders found'}, status=status.HTTP_404_NOT_FOUND)

    # GET for Stakeholder
    if request.method == 'GET':
        # get Stakeholder via "Find all objects by condition"
        stakeholders = Stakeholder.objects.filter(anwendung__name=anwendung_name)
        stakeholder_serializer = StakeholderSerializer(stakeholders, many=True)
        return JsonResponse(stakeholder_serializer.data, status=status.HTTP_200_OK, safe=False)

    # POST for Stakeholder
    # TODO: Potentially, anwendung_name should be used as part of this as well to be inserted before serialization
    # For that, see https://sunscrapers.com/blog/the-ultimate-tutorial-for-django-rest-framework-functional-endpoints-and-api-nesting-part-6/
    elif request.method == 'POST':
        stakeholder_data = JSONParser().parse(request)
        stakeholder_serializer = StakeholderSerializer(data=stakeholder_data)
        if stakeholder_serializer.is_valid():
            stakeholder_serializer.save()
            return JsonResponse({},status=status.HTTP_201_CREATED)
        else:
            # This should NOT return the errors to not reveal internal server errors. Instead this SHOULD be logged. But this is the insecure first version.
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    # Delete for Stakeholders with condition
    elif request.method == 'DELETE':
        # get Stakeholder via "Find all objects by condition"
        Stakeholder.objects.filter(anwendung__name=anwendung_name).delete()
        return JsonResponse({'message':'objects deleted'}, status=status.HTTP_200_OK)

    # block for any other methods. This should be blocked by the api_view spec, but as a doc / security measure:
    else:
        return JsonResponse({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# endpoint for Stakeholder details
@api_view(['GET', 'PUT', 'DELETE'])
def anwendung_stakeholder_details(request, anwendung_name, stakeholder_name):
    # get all appliceable stakeholders first
    try:
        stakeholders = Stakeholder.objects.filter(name=stakeholder_name, anwendung__name=anwendung_name)
    except Stakeholder.DoesNotExist:
        return JsonResponse({'message':'no matching stakeholder for name and application found'}, status=status.HTTP_404_NOT_FOUND)

    # GET for Stakeholder with condition
    if request.method == 'GET':
        stakeholder_serializer = StakeholderSerializer(stakeholders)
        return JsonResponse(stakeholder_serializer.data, status=status.HTTP_200_OK)

    # PUT for Stakeholder
    elif request.method == 'PUT':
        stakeholder_data = JSONParser().parse(request)
        stakeholder_serializer = StakeholderSerializer(stakeholders, data=stakeholder_data)
        if stakeholder_serializer.is_valid():
            stakeholder_serializer.save()
            # Theoretically one could respond with the data sent. We don't do so here because of reflection attacks
            return JsonResponse({}, status=status.HTTP_202_ACCEPTED)
        else:
            # This should NOT return the errors to not reveal internal server errors. Instead this SHOULD be logged. But this is the insecure first version.
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE for Stakeholder with conditions
    elif request.method == 'DELETE':
        stakeholders.delete()
        return JsonResponse({'message': 'Stakeholder was deleted successfully!'}, status=status.HTTP_200_OK)

    # block for any other methods. This should be blocked by the api_view spec, but as a doc / security measure:
    else:
        return JsonResponse({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'DELETE'])
def anwendung_motivation_list(request, anwendung_name):
    # This is only done here to catch cases where the declared Anwendung does not exist
    try:
        anwendung_object = Anwendung.objects.get(name=anwendung_name)
    except Anwendung.DoesNotExist:
        return JsonResponse({'message': 'the requested object does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # GET for Motivation
    if request.method == 'GET':
        # get Motivation via "Find all objects by condition"
        motivations = Motivation.objects.filter(anwendung__name=anwendung_name)
        motivation_serializer = MotivationSerializer(motivations, many=True)
        return JsonResponse(motivation_serializer.data, status=status.HTTP_200_OK, safe=False)

    # POST for Motivation
    # TODO: Potentially, anwendung_name should be used as part of this as well to be inserted before serialization
    # For that, see https://sunscrapers.com/blog/the-ultimate-tutorial-for-django-rest-framework-functional-endpoints-and-api-nesting-part-6/
    elif request.method == 'POST':
        motivation_data = JSONParser().parse(request)
        motivation_serializer = MotivationSerializer(data=motivation_data)
        if motivation_serializer.is_valid():
            motivation_serializer.save()
            return JsonResponse({},status=status.HTTP_201_CREATED)
        else:
            # This should NOT return the errors to not reveal internal server errors. Instead this SHOULD be logged. But this is the insecure first version.
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    # Delete for Motivation with condition
    elif request.method == 'DELETE':
        # get Stakeholder via "Find all objects by condition"
        Motivation.objects.filter(anwendung__name=anwendung_name).delete()
        return JsonResponse({'message':'objects deleted'}, status=status.HTTP_200_OK)

    # block for any other methods. This should be blocked by the api_view spec, but as a doc / security measure:
    else:
        return JsonResponse({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# endpoint for Motivation details
@api_view(['GET', 'PUT', 'DELETE'])
def anwendung_motivation_details(request, anwendung_name, motivation_name):
    # get appliceable motivation objects first
    try:
        motivation = Motivation.objects.filter(name=motivation_name, anwendung__name=anwendung_name)
    except Motivation.DoesNotExist:
        return JsonResponse({'message':'the specified motivation does not exist (for this application)'}, status=status.HTTP_404_NOT_FOUND)

    # GET for a specific Stakeholder (Single request)
    if request.method == 'GET':
        motivation_serializer = MotivationSerializer(motivation)
        return JsonResponse(motivation_serializer.data,status=status.HTTP_202_ACCEPTED)

    # PUT for a specific Stakeholder
    elif request.method == 'PUT':
        motivation_data = JSONParser().parse(request)
        motivation_serializer = MotivationSerializer(motivation, data=motivation_data)
        if motivation_serializer.is_valid():
            motivation_serializer.save()
            return JsonResponse({}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE for a specific stakeholder
    elif request.method == 'DELETE':
        motivation.delete()
        return JsonResponse({'message':'motivation has been deleted'}, status=status.HTTP_200_OK)

    else:
        return JsonResponse({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# Endpoints for Ansatz lists
@api_view(['GET', 'POST', 'DELETE'])
def anwendung_ansatz_list(request, anwendung_name):
    # get application first to check if it exists
    try:
        anwendung = Anwendung.objects.get(name=anwendung_name)
    except Anwendung.DoesNotExist:
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

    # GET for all Ansatz
    if request.method == 'GET':
        ansaetze = Ansatz.objects.filter(anwendung__name = anwendung_name)
        ansatz_serializer = AnsatzSerializer(ansaetze, many=True)
        return JsonResponse(ansatz_serializer.data, status=status.HTTP_200_OK, safe=False)

    # POST for Ansatz
    elif request.method == 'POST':
        ansatz_data = JSONParser().parse(request)
        ansatz_serializer = AnsatzSerializer(data=ansatz_data)
        if ansatz_serializer.is_valid():
            ansatz_serializer.save()
            return JsonResponse({}, status=status.HTTP_201_CREATED)
        else:
            # This should NOT return the errors to not reveal internal server errors. Instead this SHOULD be logged. But this is the insecure first version.
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    # Delete for Motivation with condition
    elif request.method == 'DELETE':
        # get Stakeholder via "Find all objects by condition"
        Ansatz.objects.filter(anwendung__name=anwendung_name).delete()
        return JsonResponse({'message': 'objects deleted'}, status=status.HTTP_200_OK)

    # block for any other methods. This should be blocked by the api_view spec, but as a doc / security measure:
    else:
        return JsonResponse({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# endpoint for Ansatz details
@api_view(['GET', 'PUT', 'DELETE'])
def anwendung_ansatz_details(request, anwendung_name, ansatz_name):
    try:
        ansatz = Ansatz.objects.get(name = ansatz_name, anwendung__name = anwendung_name)
    except Ansatz.DoesNotExist:
        return JsonResponse({'message':'Ansatz not found for this Anwendung or overall'}, status=status.HTTP_404_NOT_FOUND)

    # GET for a specific Ansatz
    if request.method == 'GET':
        ansatz_serializer = AnsatzSerializer(ansatz)
        return JsonResponse(ansatz_serializer.data,status=status.HTTP_200_OK)

    # PUT for a specific Ansatz
    elif request.method == 'PUT':
        ansatz_data = JSONParser().parse(request)
        ansatz_serializer = AnsatzSerializer(ansatz, data = ansatz_data)
        if ansatz_serializer.is_valid():
            ansatz_serializer.save()
            return JsonResponse({}, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE fpr a specific Ansatz
    elif request.method == 'DELETE':
        ansatz.delete()
        return JsonResponse({'message':'the ansatz has been deleted'}, status=status.HTTP_200_OK)

    else:
        return JsonResponse({'message':'this method is not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED)

# Endpoints for Konsequenz lists
@api_view(['GET', 'POST', 'DELETE'])
def anwendung_motivation_konsequenz_list(request, anwendung_name, motivation_name):
    #check if the combination exists
    try:
        motivation = Motivation.objects.filter(name=motivation_name, anwendung__name = anwendung_name)
    except Motivation.DoesNotExist:
        return JsonResponse({'message':'no motivation found for this combination'}, status=status.HTTP_404_NOT_FOUND)

    # GET for Consequences
    if request.method == 'GET':
        konsequenzen = Konsequenz.objects.filter(motivation__name = motivation_name, motivation__anwendung__name = anwendung_name)
        konsequenzen_serializer = KonsequenzSerializer(konsequenzen, many=True)
        return JsonResponse(konsequenzen_serializer.data, status=status.HTTP_200_OK, safe=False)

    # POST for consequences
    elif request.method == 'POST':
        konsequenz_data = JSONParser().parse(request)
        konsequenz_serializer = KonsequenzSerializer(data=konsequenz_data)
        if konsequenz_serializer.is_valid():
            konsequenz_serializer.save()
            return JsonResponse({}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE for consequences
    elif request.method == 'DELETE':
        Konsequenz.objects.filter(motivation__name=motivation_name, motivation__anwendung__name=anwendung_name).delete()
        return JsonResponse({'message':'all konsequenzen have been deleted'}, status=status.HTTP_200_OK)

    # Backstop
    else:
        return JsonResponse({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# endpoint for Konsequenz details
@api_view(['GET', 'PUT', 'DELETE'])
def anwendung_motivation_konsequenz_details(request, anwendung_name, motivation_name, konsequenz_name):
    try:
        konsequenz = Konsequenz.objects.get(name = konsequenz_name, motivation__name = motivation_name, motivation__anwendung__name = anwendung_name)
    except Konsequenz.DoesNotExist:
        return JsonResponse({'message': 'the konsequence does not exist fro the Anwendung and Motivation specified'}, status=status.HTTP_404_NOT_FOUND)

    # GET for a specific Consequence
    if request.method == 'GET':
        konsequenz_serializer = KonsequenzSerializer(konsequenz)
        return JsonResponse(konsequenz_serializer.data, status=status.HTTP_200_OK)

    # PUT for a specific Consequence
    elif request.method == 'PUT':
        konsequenz_data = JSONParser().parse(request)
        konsequenz_serializer = KonsequenzSerializer(konsequenz, data=konsequenz_data)
        if konsequenz_serializer.is_valid():
            konsequenz_serializer.save()
            return JsonResponse({}, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE for a specific Consequence
    elif request.method == 'DELETE':
        konsequenz.delete()
        return JsonResponse({'message':'the Konsequnz has been deleted'}, status=status.HTTP_200_OK)
    # backstop
    else:
        return JsonResponse({'message':'the method is not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# Endpoints for Anforderung lists
@api_view(['GET', 'POST', 'DELETE'])
def anwendung_ansatz_anforderung_list(request, anwendung_name, ansatz_name):
    # check if the combination exists
    try:
        ansatz = Ansatz.objects.filter(name=ansatz_name, anwendung__name=anwendung_name)
    except Ansatz.DoesNotExist:
        return JsonResponse({'message': 'no motivation found for this combination'}, status=status.HTTP_404_NOT_FOUND)

    # GET for anforderungen
    if request.method == 'GET':
        anforderungen = Anforderung.objects.filter(ansatz__name = ansatz_name, ansatz__anwendung__name = anwendung_name)
        anforderung_serializer = AnforderungSerializer(anforderungen, many=True)
        return JsonResponse(anforderung_serializer.data, status=status.HTTP_200_OK, safe=False)

    # POST for anforderungen
    elif request.method == 'POST':
        ansatz_data = JSONParser().parse(request)
        ansatz_serializer = AnsatzSerializer(data=ansatz_data)
        if ansatz_serializer.is_valid():
            ansatz_serializer.save()
            return JsonResponse({}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)


    # DELETE for anforderungen
    elif request.method == 'DELETE':
        Anforderung.objects.filter(ansatz__name=ansatz_name, ansatz__anwendung__name=anwendung_name).delete()
        return JsonResponse({'message':'all Anforderungen have been deleted'}, status=status.HTTP_200_OK)

    # Backstop
    else:
        return JsonResponse({'message':'method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# endpoint for Anforderung details
@api_view(['GET', 'PUT', 'DELETE'])
def anwendung_ansatz_anforderung_details(request, anwendung_name, ansatz_name, anforderung_name):
    try:
        anforderung = Anforderung.objects.get(name = anforderung_name, ansatz__name = ansatz_name, ansatz_anwendung__name = anwendung_name)
    except Anforderung.DoesNotExist:
        return JsonResponse({'message': 'ansatz not found'}, status=status.HTTP_404_NOT_FOUND)

    # GET for a specific Anforderung
    if request.method == 'GET':
        anforderun_serializer = AnforderungSerializer(anforderung)
        return JsonResponse(anforderun_serializer.data, status=status.HTTP_200_OK)

    # PUT for a specific Anforderung
    elif request.method == 'PUT':
        anforderung_data = JSONParser().parse(request)
        anforderung_serializer = AnforderungSerializer(anforderung, data=anforderung_data)
        if anforderung_serializer.is_valid():
            anforderung_serializer.save()
            return JsonResponse({}, status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE for a specific Anfoderung
    elif request.method == 'DELETE':
        anforderung.delete()
        return JsonResponse({'message': 'the Ansatz has been deleted'}, status=status.HTTP_200_OK)

    # Backstop
    else:
        return JsonResponse({'message': 'method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)