from django.conf.urls.defaults import *
from accounts.views import Register


urlpatterns = patterns('',
                       url(r'^reg$', Register.as_view(), name="account_reg"),
                       url(r'^doReg$', view="accounts.views.do_reg", name="account_doReg"),
                       url(r'^manager$', view="accounts.views.manager", name="account_manager"),
                       url(r'^allow$', view="accounts.views.allow", name="account_allow"),
)