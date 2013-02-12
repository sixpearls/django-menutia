#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.template.loader import render_to_string
from menutia import settings # cache menus?
from menutia.models import Menu, MenuItem
from django.utils.safestring import mark_safe
# also add a jQuery ul menu --> dropdown select tag

register = template.Library()

@register.simple_tag(takes_context=True)
def show_menu(context,menu_title=''):
    """
        {% load menutia_tags  %}
        {% show_menu 'main' %}
    """
    this_menu = Menu.objects.get(title=menu_title)
    menu_items = MenuItem.objects.filter(menu=this_menu)
    content = ''
    for menu_item in menu_items:
        menu_item.selected = menu_item.match(context['request'].path)
        extra_content = ''
        for child_menu in menu_item.child_menus.all():
            extra_content += show_menu(context,child_menu.title)
        content += render_to_string('menutia/menu_li.html',
            {'Item' : menu_item, 'Menu' : this_menu, 'extra_content': mark_safe(extra_content) })
    result = render_to_string('menutia/menu_ul.html',{'content' : mark_safe(content), 'Menu' : this_menu, })
    return result
