
from django.conf.urls import patterns, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
                       (r'^admin/', include(admin.site.urls)),
                       (r'^', include('alipay_python.accounts.urls')),
                       (r'^', include('alipay_python.payment.urls')),
)

urlpatterns += staticfiles_urlpatterns()