from django.template.defaulttags import register


@register.filter
def get_dict_value(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key, None)


@register.filter(name='get_list_value')
def get_list_value(list_obj, num):
    """Получает значение по индексу из списка."""
    return list_obj[num]


@register.filter(name='is_member')
def is_member(user, group):
    """Проверяет явлется пользователь участником группы."""
    return user.groups.filter(name=group).exists()
