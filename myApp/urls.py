# encoding:utf-8
# /usr/bin/env python
"""
@version: 1.0
@author:Jacky
@file:urls.py
#time:2019/11/7 22:17
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('login/', views.login),
    path('doLogin/', views.doLogin),

    # Admin
    path('myApp/Admin/check/', views.admincheck),

    # 一级管理员添加通知
    path('myApp/Admin/addInfo', views.addInfo),
    # 一级管理员查询通知
    path('myApp/Admin/checkInfo', views.checkinfo),
    # 一级管理员删除通知
    path('myApp/Admin/deleteinfo', views.deleteinfo),

    # 注册二级管理员
    path('myApp/Admin/registerManager', views.registerManager),
    # 查询二级管理员账户信息
    path('myApp/Admin/managerlist', views.managerlist),
    # 删除二级单位账号
    path('myApp/Admin/deleteManager', views.deleteManager),


    # 一级管理员查看某二级单位候选人的投票结果
    path('myApp/Admin/checkresult', views.checkresult),
    # 一级管理员查看某二级单位的投票情况
    path('myApp/Admin/checksecondresult', views.checkSecondResult),

    # 添加候选人页面
    path('myApp/Admin/canditate/', views.canditate),
    # 添加候选人接口
    path('myApp/Admin/addcanditate', views.addCanditate),
    # 查看候选人名单
    path('myApp/Admin/showcanditate', views.showcanditate),
    # 提交候选人结果
    path('myApp/Admin/canditatefeedback', views.canditatefeedback),
    # 实时查询已评议账号
    path('myApp/Admin/finishlist', views.finishlist),
    # 实时查询未评议账号
    path('myApp/Admin/unfinishlist', views.unfinishlist),

    path('myApp/Admin/ctl/', views.adminctl),
    path('myApp/Admin/inform/', views.admininform),
    path('myApp/Admin/register/', views.adminregister),
    path('myApp/Admin/result/', views.adminresult),


    # Manager

    # 创建普通用户
    path('myApp/Manager/registerUser', views.registerUser),
    # 显示普通用户
    path('myApp/Manager/userList', views.userList),
    # 删除普通用户
    path('myApp/Manager/deleteUser', views.deleteUser),
    path('myApp/Manager/addpeople/', views.manaddpeople),


    path('myApp/Manager/check/', views.mancheck),
    path('myApp/Manager/inform/', views.maninform),
    path('myApp/Manager/register/', views.manregister),
    path('myApp/Manager/result/', views.manresult),

    # User
    path('myApp/User/acceptinfo/', views.useacceptinfo),
    path('myApp/User/newselect/', views.usenew),
    path('myApp/User/usepeople/', views.usepeople),

    # 二级单位选人用人工作评议结果反馈表
    path('myApp/User/selectapoint', views.selectAppoint),
]