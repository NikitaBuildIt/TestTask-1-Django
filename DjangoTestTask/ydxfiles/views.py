from django.shortcuts import render
from django.http import JsonResponse
from loguru import logger
from .library import api_client
from django.core.cache import cache

def get_files(public_key: str) -> list: #простое кеширование при помощи Django.cache
    files = cache.get(public_key)
    if not files:
        files = api_client.ApiClient().main(public_key=public_key)
        cache.set(public_key, files, timeout=300)
    return files

def index(request):
    if request.method == 'POST':
        public_key = request.POST.get('url', '')
        files_list = get_files(public_key=public_key)

        return JsonResponse({'files': files_list})

    return render(request, 'ydxfiles/index.html', {'files': []})
