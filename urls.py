from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views as auth_views
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'lbform.views.home', name='home'),
	url(r'^search/$', 'lbform.views.search', name='search'),
	url(r'^user_search/$', 'lbform.views.user_search', name='user_search'),
	url(r'^(?P<id>\d+)/$', 'lbform.views.page', name='page'),
	url(r'^load/$', 'lbform.views.load_articles', name='load_articles'),
	url(r'^(?P<id>\d+)/ajax_article/$', 'lbform.views.ajax_article', name='ajax_article'),
	url(r'^(?P<id>\d+)/add_comment/$', 'lbform.views.add_comment', name='add_comment'),
	url(r'^(?P<id>\d+)/load_comments/$', 'lbform.views.load_comments', name='load_comments'),
	url(r'^(?P<id>\d+)/edit_article/$', 'lbform.views.edit_article', name='edit_article'),
	url(r'^add_article/$', 'lbform.views.add_article', name='add_article'),
	url(r'^login/$','lbform.views.login_view',name='login_view'),
	url(r'^register/$','lbform.views.register_view',name='register_view'),
	url(r'^chgpassword/$','lbform.views.chgpassword_view',name='chgpassword_view'),
	url(r'^getpassword/$','lbform.views.getpassword_view',name='getpassword_view'),
    url(r'^logout/$','lbform.views.logout_view',name='logout_view'),
 

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
