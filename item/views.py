from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django_redis import get_redis_connection
from django.core.cache import cache
import random
from django.urls import reverse
import json
import uuid

from django.views.decorators.csrf import csrf_exempt
from django.core.signing import Signer

@csrf_exempt
def main(request):
    if request.method == 'POST':
        # 從 POST 請求中獲取數據
        try:
            data = json.loads(request.body)
            items = [item for item in data['items'].split(',') if item.strip()]

            # 生成 UUID
            identifier = str(uuid.uuid4())

            cache_key = f'item_set_{identifier}'

            existing_item_set = cache.get(cache_key)

            if existing_item_set:
                content = {'ok': False, 'message': f' {cache_key} 已存在資料，請更換。'}
            else:
                cache.set(cache_key, items, 3600)
                cache.set(cache_key + 'init', items, 3600)

                content = {'ok': True, 'items': cache.get(cache_key), 'identifier': identifier}

            return JsonResponse(content)
        except json.JSONDecodeError:
            # 如果解析 JSON 失敗，返回相應的錯誤
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return render(request, "item/index.html")

def item_result(request, identifier):

    cache_key = f'item_set_{identifier}'
    init_items_set = cache.get(cache_key + 'init')

    context = {
        'identifier': identifier,
        'init_items_set': init_items_set
    }
    return render(request, "item/random_item.html", context)



def item_get(request, identifier):
    cache_key = f'item_set_{identifier}'

    items_set = cache.get(cache_key, set())
    if not items_set:
        content = {'ok': False, 'message': '請初始化'}
        return JsonResponse(content)

    # 隨機取 item
    item = random.choice(list(items_set))

    # 移除剛的隨機數
    if item is not None:
        items_set.remove(item)

    # 更新 redis
    cache.set(cache_key, items_set, 3600)

    content = {'ok': True, 'random_item': item}
    return JsonResponse(content)


def item_show(request, identifier):

    cache_key = f'item_set_{identifier}'
    existing_items_set = cache.get(cache_key)
    if existing_items_set:
        content = {'ok': True, 'items_set': cache.get(cache_key)}
    else:
        content = {'ok': False, 'items_set': cache.get(cache_key)}

    return JsonResponse(content)


def item_init(request, identifier):

    cache_key = f'item_set_{identifier}'
    existing_items_set = cache.get(cache_key)

    if existing_items_set:
        content = {'message': f' {cache_key} 已存在資料，不能初始化。'}
    else:
        init_items_set = cache.get(cache_key + 'init')

        cache.set(cache_key, init_items_set, 3600)
        content = {'ok': True, 'items_set': cache.get(cache_key)}

    return JsonResponse(content)


def url_check(request, identifier):

    cache_key = f'item_set_{identifier}'
    init_items_set = cache.get(cache_key + 'init')

    if init_items_set:
        content = {'ok': True,}
    else:
        content = {'ok': False,}

    return JsonResponse(content)

def clear_cache(repuest):
    cache.clear()
