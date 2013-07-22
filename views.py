#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, get_object_or_404,render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.template.defaultfilters import date
from django.contrib.auth.models import User
from models import Article,Comment
from django.contrib.auth import authenticate,login,logout 
from django.utils.encoding import force_unicode
try:
    from simplejson import JSONEncoder
except ImportError:
    try:
        from json import JSONEncoder
    except ImportError:
        from django.utils.simplejson import JSONEncoder

class LazyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj



def home(request):
    template_name = 'home.html'
    objs = Article.objects.filter(status='finished')
    ctx={'objs':objs}
    return render(request, template_name, ctx)
	
def load_articles(request,data_type='json'):

    rows = []
    objs = Article.objects.filter(status='finished')
    for obj in objs:            
		row = {}
		row['id'] = obj.id
		row['name'] = obj.name
		row['created_by'] = obj.created_by.username
		row['count'] = obj.comment_set.count()
		row['date'] = date(obj.updated_on, 'Y-m-d') if obj.updated_on else "",
		rows.append(row)    
    data = {
            'rows': rows,
            'records': len(rows),
        }
    return HttpResponse(LazyEncoder().encode(data), mimetype='application/json')
 

def search(request):
    template_name = 'home.html'
    title = request.POST.get('title','')
    objs = Article.objects.filter(status='finished')
    objs = objs.filter(Q(name__icontains=title)|Q(content__icontains=title))
    ctx={'objs':objs}
    return render(request, template_name, ctx) 
def user_search(request):
    template_name = 'home.html'
    objs = Article.objects.filter(status='finished')
    print request.user
    objs = objs.filter(created_by=request.user)
    print objs,
    ctx={'objs':objs}
    return render(request, template_name, ctx) 
 
def page(request,id):
    template_name = 'page.html'
    obj=get_object_or_404(Article,id=id)
    ctx={'obj':obj}
    return render(request, template_name, ctx)
def ajax_article(request,id,data_type='json'):

	obj=get_object_or_404(Article,id=id)          
	row = {}
	row['id'] = obj.id
	row['content'] = obj.content
	row['name'] = obj.name
	row['created_by'] = obj.created_by.username
	row['created_on'] = date(obj.updated_on, 'Y-m-d') if obj.updated_on else "",  
	data = {
			'row': row,
			'records': len(row),
		}
	return HttpResponse(LazyEncoder().encode(data), mimetype='application/json')
def load_comments(request,id,data_type='json'):

	rows = []
	article=get_object_or_404(Article,id=id)
	objs = article.comment_set.all()
	for obj in objs:            
		row = {}
		row['id'] = obj.id
		row['name'] = obj.name
		row['content'] = obj.content
		row['created_by'] = obj.created_by.username if obj.created_by else ""
		row['created_on'] = date(obj.updated_on, 'Y-m-d') if obj.updated_on else ""
		rows.append(row)    
	data = {
			'rows': rows,
			'records': len(rows),
		}
	return HttpResponse(LazyEncoder().encode(data), mimetype='application/json')
 

@csrf_exempt
def add_article(request):
	info = ''
	name = request.POST.get('name','')
	content = request.POST.get('content','')
	if not name or not content:
		info = u"标题与内容不能为空"
	else:
		if not request.user.is_authenticated():
			info = u"请登录"  
		article = Article(name=name,content=content,status="finished")      
		article.created_by = request.user 
		article.save()
		info = u"发表成功"
		
	data={'info':info}
	return HttpResponse(LazyEncoder().encode(data), mimetype='application/json')
@csrf_exempt
def edit_article(request,id):
	info = ''
	article=get_object_or_404(Article,id=id)
	name = request.POST.get('name','')
	content = request.POST.get('content','')
	if not name or not content:
		info = u"标题与内容不能为空"
	else:
		if not request.user.is_authenticated():
			info = u"请登录"       
		article.name = name
		article.content = content
		article.save()
		info = u"发表成功"
		
	data={'info':info}
	return HttpResponse(LazyEncoder().encode(data), mimetype='application/json')
	
@csrf_exempt
def add_comment(request,id):
    info = ''
    obj=get_object_or_404(Article,id=id)
    name = request.POST.get('name','')
    content = request.POST.get('content','')
    if not content:
	
        info = u"评论为空"
    else:
        if not name and not request.user.is_authenticated():
            name = u"匿名"    
        com = Comment(name=name,content=content)
        com.article = obj
        if request.user.is_authenticated():
            com.created_by = request.user 
        com.save()
        info = u"添加成功"
    data = {'info':info}
    return HttpResponse(LazyEncoder().encode(data), mimetype='application/json')

def register_view(request):
	ctx={}
	template_name = 'register.html'
	if request.POST:
		username = request.POST.get('username',None)
		email = request.POST.get('email',None)
		password = request.POST.get('password',None)
		user = User.objects.create_user(username, email, password)
		if user:
			user.save()
			n_user = authenticate(username=user.username,password=password)  
			if n_user :
				login(request, n_user)
			return HttpResponseRedirect(reverse("home")) 
	return render(request, template_name, ctx)
def chgpassword_view(request):
	ctx={}
	template_name = 'chgpassword.html'
	user = request.user
	if request.POST:
		password1 = request.POST.get('password',None)
		password2 = request.POST.get('repassword',None)
		if password1 and password1 == password2:
			user.set_password(password1)
			user.save()
			return HttpResponseRedirect(reverse("home")) 
	return render(request, template_name, ctx)
	

def getpassword_view(request):
	ctx={}
	template_name = 'getpassword.html'
	if request.POST:
		username = request.POST.get('username',None)
		email = request.POST.get('email',None)
		user = User.objects.get(username=username, email=email)
		user.set_password("system")
		user.save()
		n_user = authenticate(username=user.username, password="system")  
		if n_user: 
			login(request, n_user)
			return HttpResponseRedirect(reverse("chgpassword_view")) 
	return render(request, template_name, ctx)
	
def login_view(request):
	ctx={}
	template_name = 'login.html'
	if request.POST:
		user = authenticate(username=request.POST['username'], password=request.POST['password'])  
		if user :  
			login(request, user)
			return HttpResponseRedirect(reverse("home")) 
	return render(request, template_name, ctx)
  
def logout_view(request): 
	logout(request)  
	return HttpResponseRedirect(reverse("home"))