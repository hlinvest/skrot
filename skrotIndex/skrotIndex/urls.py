# -*- coding: utf-8 -*-  
from django.conf.urls import patterns, include, url
from django.contrib import admin
from skrotIndex import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns('ao.views',
    # url(r'^skrotIndex/', include('skrotIndex.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'index'),
    (r'^register/$','register'),  
    (r'^login/$','userLogin'),
    (r'^login/(?P<carid>.*)','userLogin'),
    (r'^profil/$','profile'),
    (r'^redigere_profil/$','editProfile'),
    (r'^logud/$','userLogout'),
    (r'^auto_ophugger/$', 'index'),
    (r'^auto_ophugger/(?P<area>[\w|\W]+)/$', 'index'),
    (r'^ophugger/(?P<id>.*)/$','ophugger'),
    (r'^redigere_profile_billede/$','editPic'),
    (r'^vil_du_slet_profil/$','willDeleteProfile'),
    (r'^slet_profil/$','deleteProfile'),
)
urlpatterns+=patterns('cars.views',
            url(r'^skrot/$','skrot'),
            (r'^biler/(?P<area>[\w|\W]+)/$', 'biler'),
            (r'^biler/$', 'biler'),
            (r'^bil/(?P<carid>.*)/$', 'bil'), 
            (r'^bekraeft_slet_bud/(?P<bidID>.*)/$', 'confirmDeleteBid'), 
            (r'^slet_bud/(?P<bidID>.*)/$', 'deleteBid'),  
    
)
urlpatterns+=patterns('',
     url(r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
     (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
     (r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
     (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
     )+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+staticfiles_urlpatterns()
