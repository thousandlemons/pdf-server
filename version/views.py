from django.shortcuts import render

# Create your views here.
import json

from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from version.models import Version
from version.serializers import VersionSerializer

class VersionList(APIView):
    def get(self, request, format=None):
    

class VersionDetail(APIView):
    def get(self, request, pk, format=None):
    

class VersionCreate(APIView):
    def post(self, request, format=None):
    

class VersionUpdate(APIView):
    def post(self, request, pk, format=None):
    

class VersionDelete(APIView):
    def post(self, request, pk, format=None):
