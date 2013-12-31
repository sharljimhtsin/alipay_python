from django.db.models import Max
from django.db.models.query import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from models import Partner
import random
import string

__author__ = 'sharl'

_TYPE_GAME = 0
_TYPE_MUSIC = 1
_TYPE_LIVE = 2
_TYPE_TRANSPORT = 3


class Register(TemplateView):
    template_name = "reg.html"


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def do_reg(request):
    if not request.POST:
        return HttpResponse("error")

    partner = Partner(name=request.POST.get('username'),
                      app_name=request.POST.get('appname'),
                      company_name=request.POST.get('companyname'),
                      email=request.POST.get('email'),
                      phone=request.POST.get('phone'),
                      notify_url=request.POST.get('notifyurl'),
                      app_type=request.POST.get('apptype'),
                      app_id=gen_app_id(request.POST.get('apptype')),
                      app_key=gen_app_key(),
    )
    partner.save()
    return render_to_response("waitting.html")

def gen_app_id(type):
    type = int(type)
    max_id = Partner.objects.filter(app_type=type).aggregate(Max('app_id'))['app_id__max']
    if max_id is None:
        if type == _TYPE_GAME:
            max_id = 1000
        elif type == _TYPE_MUSIC:
            max_id = 2000
        elif type == _TYPE_LIVE:
            max_id = 3000
        elif type == _TYPE_TRANSPORT:
            max_id = 4000
    else:
        max_id += 1
    return max_id

def gen_app_key():
    strs = string.ascii_uppercase + string.ascii_lowercase + string.digits
    while True:
        id = "".join(random.sample(strs, 10))
        partner = Partner.objects.filter(app_key=id)
        if not partner:
            return id


@csrf_exempt
@require_http_methods(['GET' , 'POST'])
def manager(request):
    all = request.GET.get('all')
    keyword = request.GET.get('keyword')
    partner = None
    if keyword:
        partner = Partner.objects.filter(Q(name__contains=keyword) | Q(email__contains=keyword) | Q(app_name__contains=keyword) | Q(company_name__contains=keyword))
    elif all:
        partner = Partner.objects.all()
    else:
        partner = Partner.objects.filter(real=0)
    return render_to_response("manager.html", {"partner": partner})


@csrf_exempt
@require_http_methods(['GET'])
def allow_user(request):
    id = request.GET.get('app_id')
    partner = Partner.objects.get(app_id=id)
    if partner and partner.real == 0:
        partner.real = 1
        partner.save()
        return HttpResponse(
            "allowed,do not forget to notify partner about <br/> his appid: " + str(partner.app_id) + "<br/> his appkey: " + partner.app_key + "<br/> via his email: " + partner.email)
    return HttpResponse("no found")

@csrf_exempt
@require_http_methods(['GET'])
def deny_user(request):
    id = request.GET.get('app_id')
    partner = Partner.objects.get(app_id=id)
    if partner and partner.real == 0:
        partner.real = 2
        partner.save()
        return HttpResponse("denied")
    return HttpResponse("no found")
