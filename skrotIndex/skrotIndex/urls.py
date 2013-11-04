from django.conf.urls import patterns, include, url
from django.contrib import admin
from skrotIndex import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# admin.autodiscover()

urlpatterns = patterns('ao.views',
    # url(r'^skrotIndex/', include('skrotIndex.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'index'),
    (r'^register/$','register'),  
    (r'^login/$','userLogin'),
    (r'^profil/$','profile'),
    (r'^redigere_profil/$','eidtProfile'),
    (r'^logud/$','userLogout'),
    (r'^auto_ophugger/(?P<area>[\w|\W]+)/$', 'index'),
    
)
urlpatterns+=patterns('cars.views',
            url(r'^skrot/$','skrot'),
            (r'^biler/(?P<area>[\w|\W]+)/$', 'biler'),
            (r'^biler/$', 'biler'),
            (r'^bil/(?P<id>.*)/$', 'bil'),
    
    
)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+staticfiles_urlpatterns()
