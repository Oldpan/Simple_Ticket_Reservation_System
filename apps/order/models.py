"""
订票系统-数据库类型定义部分
使用数据库 mysql
--------------------------------
定义数据类型：1、订票类型 2、会员类型
"""

from django.db import models
from datetime import datetime


class Tickets(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"车票名称")
    num = models.CharField(default='K100', max_length=10, verbose_name=u"车票编号")
    time = models.DateTimeField(verbose_name=u"车票出发时间")
    brief = models.TextField(max_length=300, verbose_name=u"车票信息")
    seats = models.IntegerField(default=0, verbose_name=u"剩余座位")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "车票信息"
        verbose_name_plural = verbose_name


class Person(models.Model):
    name = models.CharField(max_length=10, verbose_name=u"乘客名称")
    phone_number = models.CharField(max_length=11, verbose_name=u"电话号码")
    ticket_name = models.CharField(default=' ', max_length=30, verbose_name=u"购买车票名称") # 实际存储为车次，非车票名称
    ticket_time = models.DateTimeField(default=datetime.now(), verbose_name=u"购买车票时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "乘客信息"
        verbose_name_plural = verbose_name


# Create your models here.
