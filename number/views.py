from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django.core.cache import cache
import random
import json
import uuid
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def main(request):
    if request.method == 'POST':
        # 從 POST 請求中獲取數據
        try:
            data = json.loads(request.body)

            # 生成 UUID
            identifier = str(uuid.uuid4())

            cache_key = f'number_set_{identifier}'

            existing_numbers_set = cache.get(cache_key)

            if existing_numbers_set:
                content = {'ok': False, 'message': f' {cache_key} 已存在資料，請更換。'}
            else:
                numbers = list(range(1, int(data['numCount']) + 1))
                cache.set(cache_key, numbers, 3600)
                cache.set(cache_key + 'init', numbers, 3600)

                content = {'ok': True, 'numbers': cache.get(cache_key), 'identifier': identifier}

            return JsonResponse(content)
        except json.JSONDecodeError:
            # 如果解析 JSON 失敗，返回相應的錯誤
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return render(request, "number/index.html")

def random_number(request, identifier):
    cache_key = f'number_set_{identifier}'
    init_numbes_set = cache.get(cache_key + 'init')

    context = {
        'init_numbes_set': init_numbes_set,
        'identifier': identifier,
    }
    return render(request, "number/random_number.html", context)

def number_get(request, identifier):
    cache_key = f'number_set_{identifier}'

    number_set = cache.get(cache_key, set())
    if not number_set:
        content = {'message': '請初始化'}
        return JsonResponse(content)

    # 隨機取數字
    random_number = random.choice(list(number_set)) if number_set else None

    # 移除剛的隨機數
    if random_number is not None:
        number_set.remove(random_number)

    # 更新 redis
    cache.set(cache_key, number_set, 3600)

    content = {'ok': True, 'random_number': random_number}
    return JsonResponse(content)


def number_show(request, identifier):
    cache_key = f'number_set_{identifier}'

    existing_numbers_set = cache.get(cache_key)
    if existing_numbers_set:
        content = {'ok': True, 'number_set': cache.get(cache_key)}
    else:
        content = {'ok': False, 'number_set': cache.get(cache_key)}

    return JsonResponse(content)


def number_init(request, identifier):
    cache_key = f'number_set_{identifier}'

    existing_number_set = cache.get(cache_key)

    if existing_number_set:
        content = {'message': f' {cache_key} 已存在資料，不能初始化。'}
    else:
        init_numbers_set = cache.get(cache_key + 'init')
        cache.set(cache_key, init_numbers_set, 3600)
        content = {'ok': True, 'number_set': cache.get(cache_key)}

    return JsonResponse(content)

def url_check(request, identifier):

    cache_key = f'number_set_{identifier}'
    init_numbers_set = cache.get(cache_key + 'init')

    if init_numbers_set:
        content = {'ok': True,}
    else:
        content = {'ok': False,}

    return JsonResponse(content)

def clear_cache(repuest):
    cache.clear()
