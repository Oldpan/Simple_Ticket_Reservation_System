"""
订票系统-表单处理部分
--------------------------------
"""

from django import forms
from .models import Person


# 预订车票填写信息Form
class TicketForm(forms.Form):

    name = forms.CharField(label='name', max_length=10, error_messages={'required': '请填写您的姓名',
                                                                        'max_length': '名字太长了'})
    phone_number = forms.CharField(label='phone_number', min_length=11, max_length=11,
                                   error_messages={'required': '手机号码输入不正确',
                                                   'min_length': '您输入的号码数不符合11位',
                                                   'max_length': '您输入的号码数不符合11位'})
    ticket_num = forms.CharField(label='ticket_num', max_length=10, error_messages={'required': '车票编号输入不正确'})
    # 因为预订车票车次已经足够，车票时间有些多余，所以删掉
    # ticket_time = forms.DateTimeField(label='ticket_time', error_messages={'required': '车票时间输入不正确'})


# 查询信息填写Form
class PersonForm(forms.Form):
    name = forms.CharField(label='name', max_length=10, error_messages={'required': '请填写您的姓名',
                                                                        'max_length': '名字太长了'})
    phone_number = forms.CharField(label='phone_number', min_length=11, max_length=11,
                                   error_messages={'required': '请输入手机号码',
                                                   'min_length': '您输入的号码数不符合11位',
                                                   'max_length': '您输入的号码数不符合11位'})

