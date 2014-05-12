#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.template.loader import render_to_string
from menutia import settings # cache menus?
from menutia.models import Menu, MenuItem
from django.utils.safestring import mark_safe
from django.conf import settings
# also add a jQuery ul menu --> dropdown select tag

register = template.Library()

@register.simple_tag(takes_context=True)
def show_menu(context,menu_title='',extra_lis=''):
    """
        {% load menutia_tags  %}
        {% show_menu 'main' %}
    """
    this_menu = Menu.objects.get(title=menu_title)
    content = ''
    try:
        path = context['request'].path
    except:
        path = u''
    for menu_item in this_menu.menu_items.all():
        menu_item.selected = menu_item.match(path)
        extra_content = ''
        for child_menu in menu_item.child_menus.all():
            extra_content += show_menu(context,child_menu.title)
        content += render_to_string('menutia/menu_li.html',
            {'Item' : menu_item, 'Menu' : this_menu, 'extra_content': mark_safe(extra_content) })
    content += mark_safe(extra_lis)
    result = render_to_string('menutia/menu_ul.html',{'content' : mark_safe(content), 'Menu' : this_menu, })
    return result