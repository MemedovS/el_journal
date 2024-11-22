from django.template.defaulttags import register

# @register.filter(name='get_dict_value')
# def get_dict_value(dictionary, key):
#     """Получает значение по ключу из словаря."""
#     return dictionary.get(key)

@register.filter
def get_dict_value(dictionary, key):
    # Проверка, что dictionary - это словарь, и ключ существует
    if dictionary is None:
        return None
    return dictionary.get(key, None)
@register.filter(name='get_list_value')
def get_list_value(list_obj, num):
    """Получает значение по индексу из списка."""
    return list_obj[num]
# @register.filter(name='get_list_value')
# def get_list_value(list_obj, num):
#     """Получает значение по индексу из списка."""
#     if list_obj is None or num < 0 or num >= len(list_obj):
#         return None  # Возвращаем None, если list_obj None или индекс вне диапазона
#     return list_obj[num]


@register.filter(name='is_member')
def is_member(user, group):
    """Проверяет явлется пользователь участником группы."""
    return user.groups.filter(name=group).exists()

