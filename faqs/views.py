from rest_framework import generics
from rest_framework.response import Response
from django.core.cache import cache
from .models import FAQ
from .serializers import FAQSerializer

class FAQListCreateAPIView(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def list(self, request, *args, **kwargs):
        lang = request.query_params.get('lang', 'en')
        cache_key = f"faq_list_{lang}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        # Not in cache, so fetch from DB
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        data = serializer.data
        cache.set(cache_key, data, 60*5)  # Cache 5 minutes
        return Response(data)

class FAQRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        lang = request.query_params.get('lang', 'en')
        cache_key = f"faq_detail_{pk}_{lang}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        data = serializer.data
        cache.set(cache_key, data, 60*5)
        return Response(data)
