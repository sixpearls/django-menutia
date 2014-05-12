#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings as site_settings
from django.utils.translation import ugettext, ugettext_lazy as _

from menutia import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
import operator
import ast

class Menu(models.Model):
    title = models.SlugField(_('title'), unique=True)
    description = models.TextField(_('description'), blank=True)

    html_id = models.CharField(_('HTML id'), max_length=255, blank=True)
    html_classes = models.CharField(_('HTML classes'), max_length=255,blank=True)
    selected_classes = models.CharField(_('HTML classes for selected elements'), max_length=255,blank=True)

    parent_menu_item = models.ForeignKey('MenuItem',related_name="child_menus",blank=True,null=True)
   
    def __unicode__(self):
        return "%s" % self.title
    
class MenuItem(models.Model):
    menu = models.ForeignKey(Menu,related_name="menu_items")
    text = models.CharField(_('text'), max_length=255, blank=True)

    order = models.IntegerField(_('order'))     
    html_id = models.CharField(_('HTML id'), max_length=255, blank=True)
    html_classes = models.CharField(_('HTML classes'), max_length=255,blank=True)
    selected_classes = models.CharField(_('HTML classes for selected elements'), max_length=255,blank=True)

    exact_match = models.BooleanField(default=True)
    url = models.CharField(_('URL'), max_length=255, blank=True)

    item_view = models.CharField(_('View to match'),blank=True,max_length=255,
        help_text='Python path to view that can be reversed')
    item_view_args = models.CharField(_('View args'),default='()',blank=True,max_length=255,
        help_text='args to pass to reverser')
    item_view_kwargs = models.CharField(_('View kwargs'),default='{}',blank=True,max_length=255,
        help_text='kwargs to pass to reverser')

    # something to make this more generic?
    item_type = models.ForeignKey(ContentType, blank=True, null=True)
    item_id = models.PositiveIntegerField(blank=True, null=True)
    item = generic.GenericForeignKey('item_type', 'item_id')

    class Meta:
        ordering = ["order"]
    
    def __unicode__(self):
        return "%s > %s" % (self.menu.__unicode__(), self.text)

    def get_match_test_function(self):
        if self.exact_match:
            return operator.__eq__
        else:
            return unicode.startswith

    @property
    def get_url(self):
        if self.url:
            return self.url
        if self.item_view:
            args = ast.literal_eval(self.item_view_args)
            kwargs = ast.literal_eval(self.item_view_kwargs)
            return reverse(self.item_view,args=args,kwargs=kwargs)
        if self.item:
            return self.item.get_absolute_url()
        else:
            return ''

    def match(self, request_url):
        tester = self.get_match_test_function()
        url = self.get_url
        return tester(request_url,url)
