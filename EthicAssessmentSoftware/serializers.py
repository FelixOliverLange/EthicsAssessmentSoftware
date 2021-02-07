from rest_framework import serializers
from EthicAssessmentSoftware.models import *

# Serializer for Anwendung
class AnwendungSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anwendung
        fields = ('name')

# Serializer for Motivation
class MotivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motivation
        fields = ('name','beschreibung','shutzklasse','prioritaet','ist_recht','anwendung')

# Serializer for Stakeholder
class StakeholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stakeholder
        fields = ('name','beschreibung','anwendung')

# Serializer for Konsequenz
class KonsequenzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Konsequenz
        fields = ('name','beschreibung','bewertung','betroffener','motivation')

# Serializer for Ansatz
class AnsatzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ansatz
        fields = ('name','beschreibung','adressiert','auswirkung','anwendung')

# Serializer for Anforderung
class AnforderungSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anforderung
        fields = ('name','beschreibung','ansatz')