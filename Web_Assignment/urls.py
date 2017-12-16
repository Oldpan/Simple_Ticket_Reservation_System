from django.contrib import admin
from django.urls import path
from apps.order import views
from apps.order.views import QueryView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.detailview, name='home'),   # 主页url
    path('order/', views.orderview, name='order'),  # 预订url
    path('query/', QueryView.as_view(), name='query'), # 查询取消订单url
    # path('unsubscribe/(?P<user>\w+)/$', views.unsubview, name='unsubscribe')
]
