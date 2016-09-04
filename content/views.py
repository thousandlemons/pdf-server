# Create your views here.
import json

from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from content.models import Content
from content.serializers import ContentSerializer

class ContentImmediate(APIView):
    def get(self, request, pk_section, pk_version= , format=None): # Default version key to be filled in.
    

class ContentAggregate(APIView):
    def get(self, request, pk_section, pk_version= , format=None): # Default version key to be filled in.
    

class ContentPost(APIView):
    def post(self, request, pk_section, pk_version, format=None):
    
    
        