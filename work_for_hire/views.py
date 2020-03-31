from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import port_folio, p_service, orders, order_chat, buyer_request
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse_lazy, reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone


def buyer_rst_show(request):
    user = request.user.username
    p_model = p_service.objects.filter(seller_id=user)
    b_model = buyer_request.objects.all()
    all_obj = {
        'p_details': p_model,
        'rst': b_model
    }
    return render(request, 'work_for_hire/seller/requests_show.html', all_obj)


def buyer_request_create(request):
    if request.method == 'POST':
        user = request.user.username
        category = request.POST['category']
        rst = request.POST['rst']
        rstfile = request.FILES['rstfile']
        print("done")
        b = buyer_request.objects.create(
            user=user,
            category=category,
            rst=rst,
            rst_attach=rstfile,
            created_by=timezone.now()
        )
        b.save()
        return redirect('buyer_rst_create')
    else:
        user = request.user.username
        b = buyer_request.objects.filter(user=user)
        return render(request, 'work_for_hire/seller/requests.html', {'rst': b})


def chatting(request, order_id):
    user = request.user.username
    if request.method == 'POST':
        text = request.POST['text']
        o = order_chat.objects.create(order_id=order_id,
                                      user=user,
                                      text=text,
                                      created_by=timezone.now())
        o.save()
        return HttpResponse(text)
    else:
        o = order_chat.objects.filter(order_id=order_id)
        chats = serializers.serialize('json', o)
        return HttpResponse(chats)


def order_show(request):
    user = request.user.username
    o = orders.objects.all()
    for o in o:
        print(o.seller)
        slr = o.seller
        buyer = o.buyer
        if slr == user:
            odr = orders.objects.filter(seller=slr)
            obj = {
                'o': odr
            }
            return render(request, 'work_for_hire/seller/order.html', obj)
        elif buyer == user:
            odr = orders.objects.filter(buyer=buyer)
            obj = {
                'o': odr
            }
            return render(request, 'work_for_hire/seller/order.html', obj)
        else:
            return HttpResponse('Failed')


def delete_services(request, su_pk):
    s = p_service.objects.filter(id=su_pk)
    s.delete()
    return redirect('seller')


def seller_services(request):
    u_id = request.user
    s = p_service.objects.filter(seller_id=u_id)
    return render(request, 'work_for_hire/seller/seller.html', {'s': s})


def deliver_success(request, o_pk):
    o = orders.objects.get(id=o_pk)
    o.delivery = 1
    o.save()
    o = orders.objects.get(id=o_pk)
    return render(request, 'work_for_hire/seller/order.html', {'o_details': o})


def order_services(request, srv_pk):
    if request.method == 'POST':
        user = request.user.username
        p = p_service
        if user != p.seller_id:
            requirement_text = request.POST['text']
            requirement_image = request.FILES['image']
            p = p_service.objects.get(id=srv_pk)
            order_title = p.title
            order_pricing = p.pricing
            slr = p.seller_id
            o = orders.objects.create(seller=slr,
                                      buyer=user,
                                      order_title=order_title,
                                      order_pricing=order_pricing,
                                      requirement=requirement_text,
                                      requirement_assets=requirement_image)
            o.save()
            # return render(request, 'work_for_hire/seller/order.html', {'o_details': o})
            return redirect('order_show')
        else:
            return HttpResponse('You can not order yourself !!!')
    else:
        o = orders.objects.get(id=srv_pk)
        return render(request, 'work_for_hire/seller/order.html', {'o_details': o})


def fetch_all(request, mdl):
    srv = mdl.objects.all()
    return render(request, 'work_for_hire/index.html', {'srv': srv})


def all_services(request):
    return fetch_all(request, mdl=p_service)


def services_pk(request, s_pk):
    if request.method == 'GET':
        service_pk = p_service.objects.filter(id=s_pk)
        return render(request, 'work_for_hire/index.html', {'service_pk': service_pk})
    else:
        return HttpResponse('PK Does not matched !')


def portfolio_show(request, u_id):
    if request.method == 'GET':
        pt = port_folio.objects.filter(user_id=u_id)
        d = serializers.serialize('json', pt)
        return HttpResponse(d)
    else:
        return HttpResponse('Do not have a portfolio')


def services_show(request, u_id):
    if request.method == 'GET':
        s = p_service.objects.filter(seller_id=u_id)
        d = serializers.serialize('json', s)
        return HttpResponse(d)
    else:
        return HttpResponse('Do not have any services')


def index(request):
    return fetch_all(request, p_service)


def seller(request):
    return render(request, 'work_for_hire/seller/base.html')


def login_user(request):
    if request.method == 'POST':
        mail = request.POST['email']
        pword = request.POST['password']
        user = get_object_or_404(User, email=mail, password=pword)
        if user is not None:
            login(request, user)
            return redirect('index')
    else:
        return HttpResponse('Invalid Password or Email....')


def register(request):
    if request.method == 'POST':
        mail = request.POST['email']
        usern = request.POST['username']
        pword = request.POST['password']
        bot = request.POST['bot']
        if bot:
            return HttpResponse("You Can't Register !")
        else:
            user = User.objects.create(username=usern, email=mail, password=pword)
            if user is not None:
                user.save()
                login(request, user)
                return redirect('index')
    else:
        return HttpResponse("Not Valid")


def logout_view(request):
    logout(request)
    return redirect('index')


def portfolio(request, up_id):
    if request.method == 'POST':
        p = port_folio.objects.filter(user_id=up_id)
        if p:
            picture = request.FILES['picture']
            skills = request.POST['skills']
            country = request.POST['country']
            degree = request.POST['degree']
            certify = request.POST['certify']
            p = port_folio.objects.get(user_id=up_id)
            p.picture = picture
            p.skills = skills
            p.country = country
            p.degree = degree
            p.certification = certify
            p.save()
            return redirect('seller')
        else:
            picture = request.FILES['picture']
            skills = request.POST['skills']
            country = request.POST['country']
            degree = request.POST['degree']
            certify = request.POST['certify']
            port_folio.objects.create(user_id=up_id, picture=picture, skills=skills, country=country, degree=degree,
                                      certification=certify)
            return redirect('seller')
    else:
        return redirect('seller')


def create_s(request, pk_create):
    if request.method == 'POST':
        p_pk = request.POST['pk']
        pone = request.FILES['pone']
        p_two = request.FILES['p_two']
        p_three = request.FILES['p_three']
        title = request.POST['title']
        category = request.POST['category']
        tags = request.POST['tags']
        pricing = request.POST['pricing']
        publish = request.POST['publish']
        description = request.POST['description']
        p = p_service.objects.get(id=p_pk)
        p.pic_first = pone
        p.pic_second = p_two
        p.pic_third = p_three
        p.title = title
        p.category = category
        p.tags = tags
        p.pricing = pricing
        p.published_date = publish
        p.description = description
        p.save()
        return redirect('seller')
    else:
        p = p_service.objects.create(seller_id=pk_create)
        p.save()
        port = p.pk
        return render(request, 'work_for_hire/seller/services_form.html', {'port': port})


def update_services(request, su_pk):
    if request.method == 'POST':
        pass
    else:
        s = p_service.objects.get(id=su_pk)
        return render(request, 'work_for_hire/seller/services_form.html', {'s': s})
