from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django.core.cache import cache
import random

def main(request):
    return render(request, "number/index.html")

def random_number(request, num_count, identifier):
    context = {
        'num_count': num_count,
        'identifier': identifier,
    }
    return render(request, "number/random_number.html", context)

def number_get(request, num_count, identifier):
    cache_key = f'number_set_{num_count}_{identifier}'

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


def number_show(request, num_count, identifier):
    cache_key = f'number_set_{num_count}_{identifier}'

    content = {'number_set': cache.get(cache_key)}
    return JsonResponse(content)


def number_init(request, num_count, identifier):
    cache_key = f'number_set_{num_count}_{identifier}'

    existing_number_set = cache.get(cache_key)

    if existing_number_set:
        content = {'message': f' {cache_key} 已存在資料，請更換。'}
    else:
        numbers = list(range(1, num_count + 1))
        cache.set(cache_key, numbers, 3600)
        content = {'ok': True, 'number_set': cache.get(cache_key)}

    return JsonResponse(content)

def clear_cache(repuest):
    cache.clear()
