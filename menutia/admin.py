#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Menu,MenuItem

class MenuItemInline(admin.TabularInline):
    model = MenuItem

class MenuAdmin(admin.ModelAdmin):
    model = Menu
    inlines = [ MenuItemInline, ]

admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem)