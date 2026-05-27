from rest_framework import serializers
from .models import ReviewDecision


class ReviewDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewDecision
        fields = '__all__'
        read_only_fields = ['created_at']
