#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings as site_settings
from django.utils.translation import ugettext, ugettext_lazy as _

from menutia import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
import operator

class MenuBase(models.Model):
    html_id = models.CharField(_('HTML id'), max_length=255, blank=True)
    html_classes = models.CharField(_('HTML classes'), max_length=255,blank=True)
    selected_classes = models.CharField(_('HTML classes for selected elements'), max_length=255,blank=True)

    class Meta:
        abstract = True

class Menu(MenuBase):
    title = models.SlugField(_('title'), unique=True)
    description = models.TextField(_('description'), blank=True)

    parent_menu_item = models.ForeignKey('MenuItem',related_name="child_menus",blank=True)
   
    def __unicode__(self):
        return "%s" % self.title
    
class MenuItem(MenuBase):
    menu = models.ForeignKey(Menu,related_name="menu_items")
    text = models.CharField(_('text'), max_length=255, blank=True)

    order = models.IntegerField(_('order'))     
    exact_match = models.BooleanField(default=True)
    url = models.CharField(_('URL'), max_length=255, blank=True)

    item_view = models.CharField(_('View to match'),blank=True,
        help_text='Python path to view that can be reversed')

    # something to make this more generic?
    item_type = models.ForeignKey(ContentType, blank=True, null=True)
    item_id = models.PositiveIntegerField(blank=True, null=True)
    item = generic.GenericForeignKey('item_type', 'item_id')

    class Meta:
        ordering = ["order"]
    
    def __unicode__(self):
        return "%s" % self.text

    def get_match_test_function(self):
        if self.exact_match:
            return operator.__eq__
        else:
            return str.startswith

    @property
    def get_url(self):
        if self.url:
            return self.url
        if self.item_view:
            return reverse(self.item_view)
        if self.item:
            return self.item.get_absolute_url()
        else:
            return ''

    def match(self, request_url):
        tester = self.get_match_test_function()
        url = self.get_url()
        return tester(request_url,url)