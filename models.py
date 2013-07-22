#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    STATUS_CHOICES =(
        (u'draft', u'草稿'),
        (u'finished', u'已发布'),
        )
    name = models.CharField(u'标题', max_length=255, blank=True,
            help_text=u'文章的标题')
    content = models.TextField(u'内容', blank=True,help_text=u'文章的内容')
    status = models.CharField(u'状态', max_length=255,default='unstarted',choices = STATUS_CHOICES)
 
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True, blank = True, null = True)
    created_by = models.ForeignKey(User)
        
    def __unicode__(self):
        return self.name



class Comment(models.Model):
	article = models.ForeignKey(Article)
	content = models.TextField(u'评论', blank=True)
	name = models.CharField(u'昵称', max_length=255, blank=True,null=True,help_text=u'用户没有登录需填，且不能修改')

	created_on = models.DateTimeField(auto_now_add = True)
	updated_on = models.DateTimeField(auto_now = True, blank = True, null = True)
	created_by = models.ForeignKey(User,null=True,blank=True)
	
	def __unicode__(self):
		return u'%s--%s'%(self.article.name,self.name)
