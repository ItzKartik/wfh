import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import port_folio, p_service, orders, order_chat, buyer_request, direct_message, inbox_members
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse_lazy, reverse
from django.utils.datastructures import MultiValueDictKeyError
import pytz
from django.utils import timezone
from tzlocal import get_localzone
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@login_required(login_url='index')
def create_inbox_members(request, people_id):
    u = request.user.username
    try:
        i = inbox_members.objects.get(people_id=people_id, user_id=u)
        if i:
            return HttpResponse("Change")
    except inbox_members.DoesNotExist:
        i_m = inbox_members.objects.create(
            people_id=people_id,
            user_id=u
        )
        i_m.save()
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "WFH - You Got A Message"
        html = """
        <html>
          <head></head>
          <body>
            <p>Go Check Your Inbox Now... To Keep your Response Rate Good To Clients</p>
          </body>
        </html>
        """
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp_server.login("guptapz111@gmail.com", "localhost@111")
        smtp_server.sendmail("noreply@gmail.com", "pgxxx55@gmail.com", msg.as_string())
        smtp_server.close()
        return HttpResponse(i_m.inbox_id)


def settings_page(request):
    user = request.user.username
    try:
        p = port_folio.objects.get(user_id=user)
        return render(request, 'work_for_hire/seller/settings.html', {'p': p})
    except EOFError:
        return render(request, 'work_for_hire/seller/settings.html')


@login_required(login_url='index')
def message_view(request):
    if request.method == "POST":
        inb = request.POST['inb']
        model = direct_message.objects.filter(inbox_id=inb)
        msg = serializers.serialize('json', model)
        return HttpResponse(msg)


@login_required(login_url='index')
def inbox_view(request):
    user = request.user.username
    if request.method == 'POST':
        inbox_id = request.POST['i_id']
        text = request.POST['i_text']
        file = request.FILES.get('i_file', False)
        d = direct_message.objects.create(
                inbox_id=inbox_id,
                user=user,
                text=text,
                attachments=file,
                datetime=timezone.now()
        )
        d.save()
        context = {
            'text': text,
            'file': d.attachments,
            'messanger': user
        }
        msg = json.dumps(context, indent=4, sort_keys=True, default=str)
        return HttpResponse(msg, content_type='application/json')
        # return HttpResponse("Message Sent !!!")
    else:
        p = inbox_members.objects.filter(people_id=user)
        u = inbox_members.objects.filter(user_id=user)
        if p or u:
            if p and u:
                obj = {
                    'people_id': p,
                    'user_id': u
                }
            elif p:
                obj = {
                    'people_id': p
                }
            else:
                obj = {
                    'user_id': u
                }
            return render(request, 'work_for_hire/inbox.html', obj)
        else:
            return render(request, 'work_for_hire/inbox.html')


@login_required(login_url='index')
def buyer_rst_show(request):
    user = request.user.username
    p_model = p_service.objects.filter(seller_id=user)
    b_model = buyer_request.objects.all()

    tm = get_localzone()
    all_obj = {
        'tm': tm,
        'p_details': p_model,
        'rst': b_model
    }
    return render(request, 'work_for_hire/seller/requests_show.html', all_obj)


@login_required(login_url='index')
def buyer_request_create(request):
    if request.method == 'POST':
        user = request.user.username
        category = request.POST['category']
        rst = request.POST['rst']
        rstfile = request.FILES['rstfile']
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
        try:
            tm = get_localzone()
            b = buyer_request.objects.filter(user=user)
            obj = {
                'b': b,
                'tm': tm
            }
            return render(request, 'work_for_hire/seller/requests.html', obj)
        except pytz.UnknownTimeZoneError:
            b = buyer_request.objects.filter(user=user)
            obj = {
                'b': b
            }
            return render(request, 'work_for_hire/seller/requests.html', obj)


@login_required(login_url='index')
def chatting(request, order_id):
    user = request.user.username
    if request.method == 'POST':
        text = request.POST['text']
        o = order_chat.objects.create(order_id=order_id,
                                      user=user,
                                      text=text,
                                      created_by=timezone.now()
                                      )
        o.save()
        return HttpResponse(text)
    else:
        return render(request, 'work_for_hire/seller/order.html')


@login_required(login_url='index')
def order_show(request):
    user = request.user.username
    slr_orders = orders.objects.filter(seller=user)
    bur_orders = orders.objects.filter(buyer=user)
    if slr_orders or bur_orders:
        if slr_orders and bur_orders:
            print('both' + user)
            obj = {
                's': slr_orders,
                'b': bur_orders
            }
        elif bur_orders:
            print('bur' + user)
            obj = {
                'b': bur_orders
            }
        else:
            print('slr' + user)
            obj = {
                'o': slr_orders
            }
        return render(request, 'work_for_hire/seller/order.html', obj)
    else:
        return render(request, 'work_for_hire/seller/order.html')


@login_required(login_url='index')
def delete_services(request, su_pk):
    s = p_service.objects.filter(id=su_pk)
    s.delete()
    return redirect('seller_services')


@login_required(login_url='index')
def seller_services(request):
    u_id = request.user
    s = p_service.objects.filter(seller_id=u_id)
    return render(request, 'work_for_hire/seller/seller.html', {'s': s})


@login_required(login_url='index')
def deliver_success(request, o_pk):
    o = orders.objects.get(id=o_pk)
    o.delivery = 1
    o.save()
    o = orders.objects.get(id=o_pk)
    return render(request, 'work_for_hire/seller/order.html', {'o_details': o})


@login_required(login_url='index')
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
            return redirect('order_show')
        else:
            return HttpResponse('You can not order yourself !!!')
    else:
        try:
            tm = get_localzone()
            o = orders.objects.get(id=srv_pk)
            chat = order_chat.objects.filter(order_id=srv_pk)
            obj = {
                'o_details': o,
                'tm': tm,
                'chat': chat
            }
            return render(request, 'work_for_hire/seller/order.html', obj)
        except pytz.UnknownTimeZoneError:
            o = orders.objects.get(id=srv_pk)
            chat = order_chat.objects.filter(order_id=srv_pk)
            obj = {
                'o_details': o,
                'chat': chat
            }
            return render(request, 'work_for_hire/seller/order.html', obj)


def services_pk(request, s_pk):
    if request.method == 'GET':
        service_pk = p_service.objects.filter(id=s_pk)
        return render(request, 'work_for_hire/gig_view.html', {'service_pk': service_pk})
    else:
        return HttpResponse('PK Does not matched !')


@login_required(login_url='index')
def portfolio_show(request, u_id):
    if request.method == 'GET':
        pt = port_folio.objects.filter(user_id=u_id)
        d = serializers.serialize('json', pt)
        return HttpResponse(d)
    else:
        return HttpResponse('Do not have a portfolio')


@login_required(login_url='index')
def services_show(request, u_id):
    if request.method == 'GET':
        s = p_service.objects.filter(seller_id=u_id)
        d = serializers.serialize('json', s)
        return HttpResponse(d)
    else:
        return HttpResponse('Do not have any services')


def index(request):
    srv = p_service.objects.all()
    return render(request, 'work_for_hire/index.html', {'srv': srv})


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


@login_required(login_url='index')
def portfolio(request, up_id):
    if request.method == 'POST':
        p = port_folio.objects.filter(user_id=up_id)
        if p:
            picture = request.FILES.get('picture', False)
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
            return redirect('settings_view')
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


@login_required(login_url='index')
def create_s(request, pk_create):
    if request.method == 'POST':
        p_pk = request.POST['pk']
        pone = request.FILES['pone']
        p_two = request.FILES['p_two']
        p_three = request.FILES['p_three']
        title = request.POST['title']
        t = "I will do " + title
        d_time = request.POST['d_time']
        category = request.POST['category']
        tags = request.POST['tags']
        pricing = request.POST['pricing']
        publish = request.POST['publish']
        description = request.POST['description']
        p = p_service.objects.get(id=p_pk)
        p.pic_first = pone
        p.pic_second = p_two
        p.pic_third = p_three
        p.title = t
        p.delivery_time = d_time
        p.category = category
        p.tags = tags
        p.pricing = pricing
        p.published_date = publish
        p.description = description
        p.save()
        return HttpResponse('Done')
    else:
        p = p_service.objects.create(seller_id=pk_create)
        p.save()
        port = p.pk
        return HttpResponse(port)
