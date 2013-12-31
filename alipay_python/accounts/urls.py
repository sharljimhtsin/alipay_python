
from alipay_python.accounts.views import Register
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^reg$', Register.as_view(), name="account_reg"),
                       url(r'^doReg$', view="alipay_python.accounts.views.do_reg", name="account_doReg"),
                       url(r'^manager$', view="alipay_python.accounts.views.manager", name="account_manager"),
                       url(r'^allow$', view="alipay_python.accounts.views.allow_user", name="account_allow"),
                       url(r'^deny$', view="alipay_python.accounts.views.deny_user", name="account_deny"),
)
