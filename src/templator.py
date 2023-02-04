# -*- coding: utf-8 -*-

from jinja2 import Template
from os.path import join, exists


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """
    file_path = join(folder, template_name)
    # Открываем шаблон по имени
    with open(file_path, encoding='utf-8') as f:
        # Читаем
        template = Template(f.read())
    # рендерим шаблон с параметрами
    return template.render(**kwargs)


def j2render(template_name, folder='templates', **kwargs):
    """Jinga2 template renderer enchanced with missing template detection"""
    file_path = join(folder, template_name)
    if not exists(file_path):  
        return '406 OK', 'Not acceptable'
    with open(file_path, encoding='utf-8') as f:
        template = Template(f.read())
    return '200 OK', template.render(**kwargs)
