"""
订票系统-视图逻辑定义部分
分别包括：信息显示view、预订车票view以及查询取消view
--------------------------------
"""

from django.shortcuts import render, redirect
from apps.order.models import Person, Tickets
from django.views import View
from .forms import TicketForm, PersonForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime


# 首页显示信息view，将所有的信息传递给主页并进行显示
def detailview(request):
    # 获取数据库中所有的信息
    tickets = Tickets.objects.all()
    persons = Person.objects.all()
    ticket_form = TicketForm()
    person_form = PersonForm()
    # 打包为dic
    content = {
        'tickets': tickets,
        'persons': persons,
        'ticket_form': ticket_form,
        'person_form': person_form,
    }
    return render(request, 'order_system.html', context=content)


# 预订车票功能view
def orderview(request):
    # 页面中有信息传递进来，此时method==POST
    if request.method == 'POST':
        # 将获取的信息进行Form处理
        ticket_form = TicketForm(request.POST)
        tickets = Tickets.objects.all()
        persons = Person.objects.all()
        person_form = PersonForm()

        content = {
            'tickets': tickets,
            'persons': persons,
            'ticket_form': ticket_form,
            'person_form': person_form,
            'order_message': ''
        }
        # 判断post过来的信息是否正确
        if ticket_form.is_valid():

            ticket = Tickets.objects.get(num=request.POST['ticket_num'])
            # 判断数据库中保存的购票记录中是否存在此人，如果存在则取出该数据赋给person，不存在则新建一个person
            person = Person.objects.create() if not Person.objects.filter(name=request.POST['name']) \
                else Person.objects.get(name=request.POST['name'])
            # 判断购票时间是否正确
            now_time = datetime.now()
            time_day = now_time.day - ticket.time.day

            if person.ticket_name == ticket.num:
                 message = '您已购买过此车票！'
            else:
                if time_day > 1:
                    message = '只能购买今天和明天的车票！'
                else:
                    if time_day == 0 and now_time.hour >= 23:
                        message = '当天车票超过晚上11点不可以进行购买'
                    else:
                        if ticket.seats >= 1:
                            message = '预订成功！'
                            ticket.seats -= 1
                            ticket.save()
                            person.name = request.POST['name']
                            person.phone_number = request.POST['phone_number']
                            person.ticket_time = ticket.time
                            person.ticket_name = request.POST['ticket_num']
                            person.save()
                        else:
                            message = '该车次暂无座位！'
                            person.delete()

            content['order_message'] = message

        return render(request, 'order_system.html', context=content)

    else:

        return HttpResponseRedirect(reverse(detailview))



# 查询订单、删除订单操作view
# 此view与之前的view不同，为class view
# 使用class view中的类变量进行表单间信息的传递
class QueryView(View):
    # 此处定义一个类变量，类变量的内存只存在一份，在所有类实例中会共享此参数
    temp = None

    def get(self,request):
        # get操作返回主页即可
        return HttpResponseRedirect(reverse(detailview))

    def post(self,request):
        if request.POST.get('submit') == 'find':

            person_form = PersonForm(request.POST)
            ticket_form = TicketForm()
            tickets = Tickets.objects.all()
            persons = Person.objects.all()

            content = {
                'tickets': tickets,
                'persons': persons,
                'ticket_form': ticket_form,
                'person_form': person_form,
                'query_message': '',
                'show': 0,
            }

            if person_form.is_valid():

                if Person.objects.filter(name=request.POST['name']):
                    # 根据传递来的post信息，过滤获得此person
                    persons = Person.objects.filter(name=request.POST['name'])
                    content['show'] = 1       # flag，若为1则在页面中显示已经查询到的信息
                    content['persons'] = persons
                    content['query_message'] = '查询成功！'
                    # 将查询信息保存到类变量中
                    QueryView.temp = request.POST['name']
                    return render(request, 'order_system.html', context=content)

                else:
                    content['query_message'] = '用户信息不存在！'
                    return render(request, 'order_system.html', context=content)

            return render(request, 'order_system.html', context=content)

        else:
            if request.POST.get('submit') == 'yes':
                # 从类变量中获取到之前传过来的查询到用户的信息
                persons = Person.objects.get(name=QueryView.temp)
                person_form = PersonForm()
                ticket_form = TicketForm()
                tickets = Tickets.objects.all()
                message = '用户订单取消成功！'

                content = {
                    'tickets': tickets,
                    'persons': persons,
                    'ticket_form': ticket_form,
                    'person_form': person_form,
                    'cansel_message': message,
                }
                # 取消订单后
                ticket = Tickets.objects.get(num=persons.ticket_name)
                ticket.seats += 1 # 座位归还
                ticket.save()
                persons.delete()  # 删除此人购买信息
                return render(request, 'order_system.html', context=content)

            else:

                return HttpResponseRedirect(reverse(detailview))


