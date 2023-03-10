# -*- coding: utf-8 -*-
from jinja2 import Template, FileSystemLoader  
from jinja2.environment import Environment
from os.path import join, exists


def render(template_name, folder='templates', **kwargs):
    """Common template loader"""
    env = Environment()
    env.loader = FileSystemLoader(searchpath=folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)


def j2render(template_name, folder='templates', **kwargs):
    """Jinga2 template renderer enchanced with missing template detection"""
    file_path = join(folder, template_name)
    if not exists(file_path):  
        return '406 OK', 'Not acceptable'
    with open(file_path, encoding='utf-8') as f:
        template = Template(f.read())
    return '200 OK', template.render(**kwargs)

