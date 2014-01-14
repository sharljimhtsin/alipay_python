from django.db.models import Max
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models.query import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic.base import TemplateView
from models import Partner
import random
import string
from django.contrib.auth.decorators import login_required

__author__ = 'sharl'

_TYPE_GAME = 0
_TYPE_APP = 1


class Register(TemplateView):
    template_name = "reg.html"
    
def user_login(request):
    return render_to_response("login.html", {})

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def do_user_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("/manager")
    return HttpResponse("FAIL")

def do_user_logout(request):
    logout(request)
    
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
    if type == _TYPE_GAME:
        max_id = Partner.objects.filter(app_type=type, app_id__startswith='yx').count()
        if max_id == 0:
            return 'yx' + str(1)
        else:
            return 'yx' + str(max_id + 1)
    elif type == _TYPE_APP:
        max_id = Partner.objects.filter(app_type=type, app_id__startswith='yy').count()
        if max_id == 0:
            return 'yy' + str(1)
        else:
            return 'yy' + str(max_id + 1)

def gen_app_key():
    strs = string.ascii_uppercase + string.ascii_lowercase + string.digits
    while True:
        id = "".join(random.sample(strs, 10))
        partner = Partner.objects.filter(app_key=id)
        if not partner:
            return id


@csrf_exempt
@require_http_methods(['GET' , 'POST'])
@login_required
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
@login_required
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
@login_required
def deny_user(request):
    id = request.GET.get('app_id')
    partner = Partner.objects.get(app_id=id)
    if partner and partner.real == 0:
        partner.real = 2
        partner.save()
        return HttpResponse("denied")
    return HttpResponse("no found")

@csrf_exempt
@require_http_methods(['GET'])
@login_required
def edit_user(request):
    id = request.GET.get('app_id')
    partner = Partner.objects.get(app_id=id)
    if partner and partner.real == 1:
        return render_to_response("edit.html", {"partner": partner})
    return HttpResponse("no found")

@csrf_exempt
@require_http_methods(['POST'])
@login_required
def save_user(request):
    id = request.POST.get('id')
    partner = Partner.objects.get(id=id)
    if partner and partner.real == 1:
        partner.app_name = request.POST.get('app_name')
        partner.company_name = request.POST.get('company_name')
        partner.notify_url = request.POST.get('notify_url')
        partner.save()
        return HttpResponse("ok")
    return HttpResponse("no found")
