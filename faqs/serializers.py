from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at']

    def get_question(self, obj):
        request = self.context.get('request', None)
        lang = request.query_params.get('lang', 'en') if request else 'en'
        return obj.get_question(lang)
