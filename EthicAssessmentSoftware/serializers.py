from rest_framework import serializers
from EthicAssessmentSoftware.models import *

# Serializer for Anwendung
class AnwendungSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anwendung
        fields = '__all__'

# Serializer for Motivation
class MotivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motivation
        fields = '__all__'

# Serializer for Stakeholder
class StakeholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stakeholder
        fields = '__all__'

# Serializer for Konsequenz
class KonsequenzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Konsequenz
        fields = '__all__'

# Serializer for Ansatz
class AnsatzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ansatz
        fields = '__all__'

# Serializer for Anforderung
class AnforderungSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anforderung
        fields = '__all__'