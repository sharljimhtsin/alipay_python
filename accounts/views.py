from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
import random
import string
from accounts.models import Partner

__author__ = 'sharl'


class Register(TemplateView):
    template_name = "reg.html"


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def do_reg(request):
    if not request.POST:
        return HttpResponse("error")

    partner = Partner(name=request.POST.get('username'),
                      app_name=request.POST.get('appname'),
                      email=request.POST.get('email'),
                      notify_url=request.POST.get('notifyid'),
                      app_id=gen_app_id()
    )
    partner.save()
    return render_to_response("waitting.html")


def gen_app_id():
    strs = string.ascii_uppercase + string.ascii_lowercase + string.digits
    while True:
        id = "".join(random.sample(strs, 10))
        partner = Partner.objects.filter(app_id=id)
        if not partner:
            return id


@csrf_exempt
@require_http_methods(['GET'])
def manager(request):
    partner = Partner.objects.filter(real=0)
    return render_to_response("manager.html", {"partner": partner})


@csrf_exempt
@require_http_methods(['GET'])
def allow(request):
    id = request.GET.get('app_id')
    partner = Partner.objects.get(app_id=id)
    if partner:
        partner.real = 1
        partner.save()
        return HttpResponse(
            "allowed,do not forget to notify partner about his appid " + partner.app_id + " via his email " + partner.email)
    return HttpResponse("no found")