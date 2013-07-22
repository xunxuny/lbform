#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.contrib import admin

from models import Article,Comment


class ArticleAdmin(admin.ModelAdmin):    
    list_display = ('name', 'status', 'created_by',)
    search_fields = ('name', 'created_by__username')

class CommentAdmin(admin.ModelAdmin):    
    list_display = ('name', 'article', )
    search_fields = ('name', 'article__name','created_by__username')

admin.site.register(Article,ArticleAdmin)
admin.site.register(Comment,CommentAdmin)
