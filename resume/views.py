from typing import Dict, Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """Main resume page"""
    context: Dict[str, Any] = {}
    return render(request, 'resume/index.html', context)


def api_docs(request: HttpRequest) -> HttpResponse:
    """Interactive API documentation page"""
    context: Dict[str, Any] = {}
    return render(request, 'resume/api_docs.html', context)


def built_with(request: HttpRequest) -> HttpResponse:
    """Built with page showing tech stack"""
    context: Dict[str, Any] = {}
    return render(request, 'resume/built_with.html', context)
