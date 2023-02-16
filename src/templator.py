# -*- coding: utf-8 -*-

from jinja2 import Template, FileSystemLoader  
from jinja2.environment import Environment
from os.path import join, exists


def render(template_name, folder='templates', **kwargs):
    """
    Минимальный пример работы с шаблонизатором
    :param template_name: имя шаблона
    :param kwargs: параметры для передачи в шаблон
    :return:
    """

    env = Environment()
    
    # Use `searchpath` param for templates folder
    env.loader = FileSystemLoader(searchpath=folder)
    template = env.get_template(template_name)
    print(kwargs)
    return template.render(**kwargs)




'''
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "template.html"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render()  # this is where to put args to the template renderer
'''

def j2render(template_name, folder='templates', **kwargs):
    """Jinga2 template renderer enchanced with missing template detection"""
    file_path = join(folder, template_name)
    if not exists(file_path):  
        return '406 OK', 'Not acceptable'
    with open(file_path, encoding='utf-8') as f:
        template = Template(f.read())
    return '200 OK', template.render(**kwargs)

