from django.shortcuts import render, redirect

# Create your views here.
from django.utils.timezone import now, localtime
from requests import session

from .models import Administrator, User, Manager, Canditate, Inform
import json
import random
import string
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import jsonpath

secondDict = {
    '安太堡露天矿': '101',
    '安家岭露天矿': '102',
    '东露天矿': '103',
    '中煤平朔集团有限公司': '11',
    '井工一矿': '201',
    '井工二矿': '202',
    '井工三矿': '203',
    '井东煤业': '204',
    '北岭煤业': '205',
    '井工设备安装中心': '206',
    '洗选中心': '300',
    '洗选中心-安太堡选煤厂': '301',
    '洗选中心-安家岭选煤厂': '302',
    '洗选中心-一号井选煤厂': '303',
    '洗选中心-二号井选煤厂': '304',
    '洗选中心-木瓜界洗煤厂': '305',
    '洗选中心-东露天选煤厂': '306',
    '原煤提运中心': '307',
    '露天设备维修中心': '401',
    '井工设备维修中心': '402',
    '动力中心': '403',
    '物资供应中心': '404',
    '信息中心': '405',
    '设备管理租赁中心': '406',
    '办公室1': '502',
    '党群工作部': '503',
    '财务资产部': '504',
    '人力资源部': '505',
    '企业文化部': '507',
    '文联1': '508',
    '规划发展部': '509',
    '企业管理部': '510',
    '监察审计部': '511',
    '法律事务部': '512',
    '工会': '513',
    '团委': '514',
    '环境保护部': '515',
    '公共关系部': '516',
    '地质测量中心': '517',
    '通风管理部': '518',
    '救护消防应急救援中心': '519',
    '工程管理部': '520',
    '机电管理部': '521',
    '总调度室': '523',
    '信息管理部': '525',
    '煤质运销中心': '526',
    '社保中心': '506',
    '招标中心': '529',
    '质监造价中心': '530',
    '电力销售有限公司': '531',
    '节能环保部1': '532',
    '办公室2': '533',
    '党委工作部': '534',
    '公司纪委': '535',
    '生产运营管理部': '536',
    '节能环保部2': '537',
    '文联2': '538',
    '地方协调中心': '539',
    '对外联络部': '540',
    '东日升煤矿项目部': '541',
    '朔南矿区开发建设指挥部': '542',
    '安太堡低热值煤发电项目部': '544',
    '路达公司': '545',
    '新开分局': '546',
    '中电神头发电有限公司': '547',
    '矿志办': '548',
    '马营堡矿建设项目部': '207',
    '山西中煤平朔能源化工有限公司': '800',
    '小回购煤业': '209',
    '山西中煤潘家窑煤业有限公司': '208',
    '平朔第一发电厂': '900',
    '生产技术管理中心': '522',
    '生活服务中心': '601',
    '车辆管理中心': '602',
    '保卫中心': '603',
    '技术中心': '604',
    '离退休职工管理中心': '605',
    '教育培训中心': '606',
    '档案馆': '607',
    '医院': '608',
    '工贸公司': '609',
    '木瓜界选煤厂': '700',
    '劣质煤项目部': '997',
    '外部租赁单位': '998',
}

def login(request):
    return render(request, 'myApp/login.html')

# 登录界面
def doLogin(request):
    print(request.POST)
    print(request.POST['account'])
    print(request.POST['password'])
    if request.method == "POST":
        adname = request.POST['account']
        adpassword = request.POST['password']
        if adname and adpassword:  # 确保用户名和密码都不为空
            adname = adname.strip()
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                admin = Administrator.objects.get(aname=adname)
            except BaseException:
                return HttpResponse('false')
            if admin.apasswd == adpassword:
                request.session['auth'] = request.POST['auth']
                request.session.set_expiry(3600 * 24)
                print(request.session['auth'])
                return HttpResponse('ok')
            else:
                return HttpResponse('false')
        else:
            return HttpResponse('false')
    else:
        return HttpResponse('false')

def addInfo(request):
    username = request.POST.get('account')
    text = request.POST.get('text')
    if(len(text)<500):
        print(username)
        obj = Inform.createInform(name=username, informT=text, createT=now())
        obj.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('false')


def checkinfo(request):
    information = Inform.objects.all().values('username', 'informtext', 'createTime')
    informationCount = len(information)
    informationJson = {
        "code": 0,
        "msg": "",
        "count": informationCount,
        "data": list(information)
    }
    informationJson = json.dumps(informationJson, cls=DjangoJSONEncoder)
    return HttpResponse(informationJson)

def deleteinfo(request):
    account = request.POST.get('account')
    text=request.POST.get('text')
    obj = Inform.objects.filter(username=account).filter(informtext = text)
    if(obj):
        obj.delete()
        return HttpResponse('ok')
    else:
        return HttpResponse('false')


# 注册二级管理员
def registerManager(request):      #需要二级单位名称,二级管理员名字，字符串类型

    secondDepart = request.POST.get('secondDepart')
    secondManagerName = request.POST.get('secondManagerName')

    if(Manager.objects.filter(mname =secondManagerName )):
        return HttpResponse('false')
    elif(len(secondManagerName)>=30):
        return HttpResponse('toolong')
    else:
        secondDepartNum = secondDict[secondDepart]
        secondDepartNum = int(secondDepartNum)
        print(secondDepart)
        register= Manager.createManager(type=2, name=secondManagerName, depart=secondDepartNum,createT=now())
        register.save()
        return HttpResponse('ok')


# 一级用户页面
def admincheck(request):
    return render(request, 'myApp/Admin/check.html')

# 一级管理员查询完成的任务的普通用户
def finishlist(request):
    secondDepart = request.GET.get('secondDepart')
    secondDepartNum = secondDict[secondDepart]
    int(secondDepartNum)
    finishUser = User.objects.filter(
        udepart=secondDepartNum).filter(
        ustatus=1).values('uname')
    print(finishUser)
    finishUserCount = len(finishUser)
    finishUserJson = {
        "code": 0,
        "msg": "",
        "count": finishUserCount,
        "data": list(finishUser)
    }
    finishUserJson = json.dumps(finishUserJson, cls=DjangoJSONEncoder)
    return HttpResponse(finishUserJson)


# 一级管理员查询未完成的任务的普通用户
def unfinishlist(request):
    secondDepart = request.GET.get('secondDepart')
    secondDepartNum = int(secondDict[secondDepart])
    unfinishUser = User.objects.filter(
        ustatus_1=False).filter(
        udepart=secondDepartNum).filter(ustatus_2=False).values('uname')
    unfinishUserCount = len(unfinishUser)
    unfinishUserJson = {
        "code": 0,
        "msg": "",
        "count": unfinishUserCount,
        "data": list(unfinishUser)
    }
    unfinishUserJson = json.dumps(unfinishUserJson, cls=DjangoJSONEncoder)
    return HttpResponse(unfinishUserJson)

def adminctl(request):
    return render(request, 'myApp/Admin/ctl.html')


# 添加候选人网页
def canditate(request):
    return render(request, 'myApp/Admin/canditate.html')

# 添加候选人接口
def addCanditate(request):
    # 需要json格式的候选人信息
    canditatesDepart =request.POST.get('cdepart')
    if(canditatesDepart==''):
        return HttpResponse('false')
    else:
        canditatesjsondata = request.POST.get('data')
        jsondata = json.loads(canditatesjsondata)
        cdepartNum = secondDict[canditatesDepart]
        cdepartNum = int(cdepartNum)
        for item in jsondata:
            obj = Canditate.objects.filter(cname=item['姓名']).filter(cgender=item['性别']).filter(cbirth=item['出生年月'])
            if(len(obj)!=0):
                return HttpResponse('has')
        for item in jsondata:

            Canditate.createCanditate(name=item['姓名'], birth=item['出生年月'], depart=cdepartNum,
                                      gender=item['性别'], jobnow=item['现任职务'], jobbef=item['原任职务'],
                                      jobnowT=item['任职时间']).save()
        return HttpResponse('ok')

# 显示候选人接口
def showcanditate(request):
    #   从session获取用户名，根据用户名获取depart
    a = request.POST.get('user')
    depart = 1111
    canditates = Canditate.objects.filter(cdepart=depart).values('cname','cgender','cbirth','cjobbef','cjobnow','cjobnowT')
    print(canditates)
    data = list(canditates)
    dataJson = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(dataJson)


# 一级管理员查询二级管理员账户
def managerlist(request):
    secondDepart = request.GET.get('secondDepart')
    secondDepartNum = int(secondDict[secondDepart])
    secondManager = Manager.objects.filter(
        mdepart=secondDepartNum).values('mname')
    secondManagerCount = len(secondManager)
    secondManagerJson = {
        "code": 0,
        "msg": "",
        "count": secondManagerCount,
        "data": list(secondManager)
    }
    secondManagerJson = json.dumps(secondManagerJson, cls=DjangoJSONEncoder)
    return HttpResponse(secondManagerJson)


# 删除二级账号
def deleteManager(request):
        idNum = request.POST.get('id')
        idNum=int(idNum)
        try:
            obj = Manager.objects.filter(mname=idNum)
            obj.delete()
            return HttpResponse('ok')
        except BaseException:
            return redirect('../../myApp/Admin/ctl')

def admininform(request):
    auth = request.session.get('auth', None)
    if(auth == "1"):
        return render(request, 'myApp/Admin/inform.html')
    else:
        return redirect('/')


# 一级管理员查看评议结果表1
def checkresult(request):
    secondDepart = request.GET.get('secondDepart')

    secondDepartNum = secondDict[secondDepart]
    secondDepartNum = int(secondDepartNum)
    result = Canditate.objects.filter(cdepart=secondDepartNum).values('cname', 'cgender', 'cbirth',
                                                                      'cjobnow', 'cjobbef', 'cjobnowT', 'cpoint_4', 'cpoint_3',
                                                                     'cpoint_2', 'cpoint_1', 'ccheck_0', 'ccheck_1', 'ccheck_2')
    resultList = list(result)
    resultCount = len(result)
    resultJson = {
        "code": 0,
        "msg": "",
        "count": resultCount,
        "data": resultList
    }
    resultJson=json.dumps(resultJson, cls=DjangoJSONEncoder)
    return HttpResponse(resultJson)


def adminregister(request):
    auth = request.session.get('auth', None)
    if (auth == "1"):
        return render(request, 'myApp/Admin/register.html')
    else:
        return redirect('/')


# 注册普通用户
def registerUser(request):
    # secondDepart = request.POST.get('secondDepart')
    secondDepartNum = 1112
    registerNum = request.POST.get('registerNumber')
    try:
        registerNum = int(registerNum)
    except BaseException:
        return HttpResponse('false')
    startNum=1000
    obj = User.objects.filter(udepart=secondDepartNum).last()
    if(obj == None):
        for num in range(int(registerNum)):
            name = int(secondDepartNum)*10000 + startNum + num
            obj = User.createUser(type=3, name=name, ucreateT=now(), depart=secondDepartNum)
            obj.save()
        return HttpResponse('ok')
    else:
        lastNumber = obj.uname
        for num in range(int(registerNum)):
            name = int(lastNumber) + num + 1
            obj = User.createUser(type=3, name=name, ucreateT=now(), depart=secondDepartNum)
            obj.save()
        return HttpResponse('ok')

# 删除普通用户
def deleteUser(request):
    uname = request.POST.get('uname')
    try:
        obj = User.objects.get(uname=uname)
    except BaseException:
        return HttpResponse('false')
    obj.delete()
    return HttpResponse('ok')


# 普通用户显示
def userList(request):
    # secondDepart = request.GET.get('secondDepart')
    secondDepartNum = 1111
    user = User.objects.filter(udepart=secondDepartNum).values('uname')
    userList = list(user)
    resultCount = len(user)
    userJson = {
        "code": 0,
        "msg": "",
        "count": resultCount,
        "data": userList
    }
    userJson = json.dumps(userJson, cls=DjangoJSONEncoder)
    return HttpResponse(userJson)



def adminresult(request):
    auth = request.session.get('auth', None)
    if(auth == "1"):
        return render(request, 'myApp/Admin/result.html')
    else:
        return redirect('/')



def checkSecondResult(request):
    return JsonResponse('ok')
# 二级用户的页面


def manaddpeople(request):
    return render(request, 'myApp/Manager/canditate.html')





def mancheck(request):
    # auth = request.session.get('auth', None)
    # if(auth==2):
    return render(request, 'myApp/Manager/check.html')


def maninform(request):
    return render(request, 'myApp/Manager/inform.html')


def manregister(request):

    return render(request, 'myApp/Manager/register.html')


def manresult(request):
    return render(request, 'myApp/Manager/result.html')


# 普通用户

def useacceptinfo(request):
    return render(request, 'myApp/User/acceptinform.html')


def usenew(request):
    return render(request, 'myApp/User/newselect.html')


def usepeople(request):
    return render(request, 'myApp/User/usepeople.html')


# 普通用户填写新选拔任用干部评议情况反馈表（对候选人填写）
def canditatefeedback(request):
    # 从session获取用户名。
    print(request.POST)
    username = 1111
    userobj = User.objects.get(uname =username)
    if(userobj.ustatus_1 == False):
        canditateFeedBackJson = request.POST.get('data')
        jsondata = json.loads(canditateFeedBackJson)
        for item in jsondata:
            obj = Canditate.objects.get(cname=item['姓名'])
            obj.cpoint_4 = obj.cpoint_4 + item['满意']
            obj.cpoint_3 = obj.cpoint_3 + item['基本满意']
            obj.cpoint_2 = obj.cpoint_2 + item['不满意']
            obj.cpoint_1 = obj.cpoint_1 + item['不了解1']

            obj.ccheck_0 = obj.ccheck_0 + item['存在']
            obj.ccheck_1 = obj.ccheck_1 + item['不存在']
            obj.ccheck_2 = obj.ccheck_2 + item['不了解2']
            obj.save()
        userobj.ustatus_1 = True
        userobj.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('resubmit')



# 普通用户填写二级单位选人用人工作评议反馈表（对二级单位填写）
def selectAppoint(request):
    uname = 1111
    obj = User.objects.get(uname=uname)
    data = request.POST.get('data')
    data = json.loads(data)      #JSON转换成字典
    if(obj.ustatus_2==True):
        obj.question1 = int(data['question1'])
        obj.question2 = int(data['question2'])
        obj.question3 = int(data['question3'])
        obj.question4 = int(data['question4'])
        obj.question5_1 = int(data['question5_1'])
        obj.question5_2 = int(data['question5_2'])
        obj.question5_3 = int(data['question5_3'])
        obj.question5_4 = int(data['question5_4'])
        obj.question5_5 = int(data['question5_5'])
        obj.question5_6 = int(data['question5_6'])
        obj.question5_7 = data['question5_7']
        obj.question5_8 = int(data['question5_8'])
        obj.question6 = data['question6']
        obj.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('resubmit')


# 显示二级单位选人用人工作评议情况反馈表问题1
def sandatable1(request):
    depart = 101  # 需从登录用户的对象里获取二级单位
    satisfied_score = len(User.objects.filter(depart=depart).filter(question1=4))
    basical_score = len(User.objects.filter(depart=depart).filter(question1=3))
    unsatisfail_score = len(User.objects.filter(depart=depart).filter(question1=2))
    unknown_score = len(User.objects.filter(depart=depart).filter(question1=1))
    dataDict = {
        "secondDepart": "安太堡露天矿",
        "satisfied_score": satisfied_score,
        "basical_score": basical_score,
        'unsatisfail_score': unsatisfail_score,
        'unknown_score': unknown_score,
    }
    datajson = json.dumps(dataDict, cls=DjangoJSONEncoder)
    return HttpResponse(datajson)


# 显示二级单位选人用人工作评议情况反馈表问题2
def sandatable2(request):
    depart = 101  # 需从登录用户的对象里获取二级单位
    satisfied_score = len(User.objects.filter(depart=depart).filter(question2=4))
    basical_score = len(User.objects.filter(depart=depart).filter(question2=3))
    unsatisfail_score = len(User.objects.filter(depart=depart).filter(question2=2))
    unknown_score = len(User.objects.filter(depart=depart).filter(question2=1))
    dataDict = {
        "secondDepart": "安太堡露天矿",
        "satisfied_score": satisfied_score,
        "basical_score": basical_score,
        'unsatisfail_score': unsatisfail_score,
        'unknown_score': unknown_score,
    }
    datajson = json.dumps(dataDict, cls=DjangoJSONEncoder)
    return HttpResponse(datajson)



# 显示二级单位选人用人工作评议情况反馈表问题3
def sandatable3(request):
    depart = 101  # 需从登录用户的对象里获取二级单位
    satisfied_score = len(User.objects.filter(depart=depart).filter(question3=4))
    basical_score = len(User.objects.filter(depart=depart).filter(question3=3))
    unsatisfail_score = len(User.objects.filter(depart=depart).filter(question3=2))
    unknown_score = len(User.objects.filter(depart=depart).filter(question3=1))
    dataDict = {
        "secondDepart": "安太堡露天矿",
        "satisfied_score": satisfied_score,
        "basical_score": basical_score,
        'unsatisfail_score': unsatisfail_score,
        'unknown_score': unknown_score,
    }
    datajson = json.dumps(dataDict, cls=DjangoJSONEncoder)
    return HttpResponse(datajson)



# 显示二级单位选人用人工作评议情况反馈表问题4
def sandatable4(request):
    depart = 101  # 需从登录用户的对象里获取二级单位
    satisfied_score = len(User.objects.filter(depart=depart).filter(question4=4))
    basical_score = len(User.objects.filter(depart=depart).filter(question4=3))
    unsatisfail_score = len(User.objects.filter(depart=depart).filter(question4=2))
    unknown_score = len(User.objects.filter(depart=depart).filter(question4=1))
    dataDict = {
        "secondDepart": "安太堡露天矿",
        "satisfied_score": satisfied_score,
        "basical_score": basical_score,
        'unsatisfail_score': unsatisfail_score,
        'unknown_score': unknown_score,
    }
    datajson = json.dumps(dataDict, cls=DjangoJSONEncoder)
    return HttpResponse(datajson)



# 显示二级单位选人用人工作评议情况反馈表问题5
def sandatable5(request):
    depart = 101  # 需从登录用户的对象里获取二级单位
    question5_1_score =len(User.objects.filter(depart=depart).filter(question5_1=1))
    question5_2_score = len(User.objects.filter(depart=depart).filter(question5_2=1))
    question5_3_score = len(User.objects.filter(depart=depart).filter(question5_3=1))
    question5_4_score = len(User.objects.filter(depart=depart).filter(question5_4=1))
    question5_5_score = len(User.objects.filter(depart=depart).filter(question5_5=1))
    question5_6_score = len(User.objects.filter(depart=depart).filter(question5_6=1))
    obj = User.objects.filter(depart=depart).filter(question5_7__isnull=False)
    if(len(obj)>0):
        for item in obj:
            advices = item.quesiton5_7 + str('\n')
    else:
        advices = ''
    question5_8_score = len(User.objects.filter(depart=depart).filter(question5_8=1))
    dataDict = {
        "secondDepart": "安太堡露天矿",
        "question5_1_score": question5_1_score,
        "question5_2_score": question5_2_score,
        'question5_3_score': question5_3_score,
        'question5_4_score': question5_4_score,
        'question5_5_score': question5_5_score,
        'question5_6_score': question5_6_score,
        'question5_7_score': advices,
        'question5_8_score': question5_8_score
    }
    datajson = json.dumps(dataDict, cls=DjangoJSONEncoder)
    return HttpResponse(datajson)


# 显示二级单位选人用人工作评议情况反馈表问题6
def sandatable6(request):
    depart = 101  # 需从登录用户的对象里获取二级单位
    question6 = User.objects.filter(depart=depart).filter(question6__isnull=False)
    if(len(question6)>0):
        for item in question6:
            advices = item.quesiton5_7 + str('\n')
    else:
        advices = ''
    dataDict = {
        "question6": question6,
    }
    datajson = json.dumps(dataDict, cls=DjangoJSONEncoder)
    return HttpResponse(datajson)


# “一报告两评议”结果反馈表一:干部选拔工作
def feedBackTable1(request):
    depart = 101  # 需从登录用户的对象里获取二级单位
    userNum = len(User.objects.filter(depart=depart).filter(ustatus_2=True))
    satisfied_score = len(User.objects.filter(depart=depart).filter(question1=4))
    satisfied_percent = round(satisfied_score/userNum, 4)
    basical_score = len(User.objects.filter(depart=depart).filter(question1=3))
    basical_percent = round(basical_score/userNum, 4)
    unsatisfail_score = len(User.objects.filter(depart=depart).filter(question1=2))
    unsatisfail_percent = round(unsatisfail_score/userNum, 4)
    unknown_score = len(User.objects.filter(depart=depart).filter(question1=1))
    unknown_percent = round(unknown_score/userNum, 4)
    average = round((satisfied_percent*100+basical_percent*60)/(1-unknown_percent),4)
    dataDict = {
        "secondDepart": "安太堡露天矿",
        "satisfied_percent": satisfied_percent,
        "basical_percent": basical_percent,
        'unsatisfail_percent': unsatisfail_percent,
        'unknown_percent': unknown_percent,
        "average":average
    }
    datajson = json.dumps(dataDict, cls=DjangoJSONEncoder)
    return HttpResponse(datajson)



# “一报告两评议”结果反馈表二
def feedBackTable2(request):

    depart = 101  # 需从登录用户的对象里获取二级单位
    userNum = len(User.objects.filter(depart=depart).filter(ustatus_2=True))
    satisfied_score = len(User.objects.filter(depart=depart).filter(question2=4))
    satisfied_percent = round(satisfied_score/userNum, 4)
    basical_score = len(User.objects.filter(depart=depart).filter(question2=3))
    basical_percent = round(basical_score/userNum, 4)
    unsatisfail_score = len(User.objects.filter(depart=depart).filter(question2=2))
    unsatisfail_percent = round(unsatisfail_score/userNum, 4)
    unknown_score = len(User.objects.filter(depart=depart).filter(question2=1))
    unknown_percent = round(unknown_score/userNum, 4)
    average = round((satisfied_percent * 100 + basical_percent * 60) / (1 - unknown_percent), 4)
    dataDict = {
        "secondDepart": "安太堡露天矿",
        "satisfied_percent": satisfied_percent,
        "basical_percent": basical_percent,
        'unsatisfail_percent': unsatisfail_percent,
        'unknown_percent': unknown_percent,
        "average": average
    }
    datajson = json.dumps(dataDict, cls=DjangoJSONEncoder)
    return HttpResponse(datajson)

# “一报告两评议”结果反馈表三
def feedBackTable3(request):

    depart = 101  # 需从登录用户的对象里获取二级单位
    userNum = len(User.objects.filter(depart=depart).filter(ustatus_2=True))
    satisfied_score = len(User.objects.filter(depart=depart).filter(question3=4))
    satisfied_percent = round(satisfied_score/userNum, 4)
    basical_score = len(User.objects.filter(depart=depart).filter(question3=3))
    basical_percent = round(basical_score/userNum, 4)
    unsatisfail_score = len(User.objects.filter(depart=depart).filter(question3=2))
    unsatisfail_percent = round(unsatisfail_score/userNum, 4)
    unknown_score = len(User.objects.filter(depart=depart).filter(question3=1))
    unknown_percent = round(unknown_score/userNum, 4)
    average = round((satisfied_percent * 100 + basical_percent * 60) / (1 - unknown_percent), 4)
    dataDict = {
        "secondDepart": "安太堡露天矿",
        "satisfied_percent": satisfied_percent,
        "basical_percent": basical_percent,
        'unsatisfail_percent': unsatisfail_percent,
        'unknown_percent': unknown_percent,
        "average": average
    }
    datajson = json.dumps(dataDict, cls=DjangoJSONEncoder)
    return HttpResponse(datajson)


# “一报告两评议”结果反馈表四
def feedBackTable4(request):
    depart = 101  #  需从登录用户的对象里获取二级单位
    userNum = len(User.objects.filter(depart=depart).filter(ustatus_2=True))
    satisfied_score = len(User.objects.filter(depart=depart).filter(question4=4))
    satisfied_percent = round(satisfied_score/userNum, 4)
    basical_score = len(User.objects.filter(depart=depart).filter(question4=3))
    basical_percent = round(basical_score/userNum, 4)
    unsatisfail_score = len(User.objects.filter(depart=depart).filter(question4=2))
    unsatisfail_percent = round(unsatisfail_score/userNum, 4)
    unknown_score = len(User.objects.filter(depart=depart).filter(question4=1))
    unknown_percent = round(unknown_score/userNum, 4)
    average = round((satisfied_percent * 100 + basical_percent * 60) / (1 - unknown_percent), 4)
    dataDict = {
        "secondDepart": "安太堡露天矿",
        "satisfied_percent": satisfied_percent,
        "basical_percent": basical_percent,
        'unsatisfail_percent': unsatisfail_percent,
        'unknown_percent': unknown_percent,
        "average": average
    }
    datajson = json.dumps(dataDict, cls=DjangoJSONEncoder)
    return HttpResponse(datajson)

# “一报告两评议”结果反馈表五
def feedBackTable5(request):
    depart = 101
    userNum = len(User.objects.filter(depart=depart).filter(ustatus_2=True))
    question5_1_score = len(User.objects.filter(question5_1=1).filter(depart=depart))
    question5_2_score = len(User.objects.filter(question5_2=1).filter(depart=depart))
    question5_3_score = len(User.objects.filter(question5_3=1).filter(depart=depart))
    question5_4_score = len(User.objects.filter(question5_4=1).filter(depart=depart))
    question5_5_score = len(User.objects.filter(question5_5=1).filter(depart=depart))
    question5_6_score = len(User.objects.filter(question5_6=1).filter(depart=depart))
    question5_8_score = len(User.objects.filter(question5_8=1).filter(depart=depart))
    question5_7_score = len(User.objects.filter(depart=depart).filter(question5_7=''))
    question6 = User.objects.filter(question6__isnull=False)
    average = round(question5_8_score/userNum, 4)
    if(len(question6)>0):
        for item in question6:
            advices = item.quesiton5_7 + str('\n')
    else:
        advices = ''
    dataDict = {
        "secondDepart": "安太堡露天矿",
        "userNum": userNum,
        "question5_1_score": question5_1_score,
        'question5_2_score': question5_2_score,
        'question5_3_score': question5_3_score,
        "question5_4_score": question5_4_score,
        'question5_5_score': question5_5_score,
        'question5_6_score': question5_6_score,
        "question5_7_score": question5_7_score,
        "question5_8_score": question5_8_score,
        "question6": advices,
        'average': average
    }
    datajson = json.dumps(dataDict, cls=DjangoJSONEncoder)
    return HttpResponse('ok')

# “一报告两评议”结果反馈表六
def feedBackTable6(request):
    depart =102
    userNum = len(User.objects.filter(depart=depart).filter(ustatus_1=True))
    satisfied_score = len(Canditate.objects.filter(depart=depart).fitler(cpoint4=1))
    satisfied_percent = round(satisfied_score / userNum, 4)
    basical_score = len(Canditate.objects.filter(depart=depart).fitler(cpoint3=1))
    basical_percent = round(basical_score / userNum, 4)
    unsatisfail_score = len(Canditate.objects.filter(depart=depart).fitler(cpoint2=1))
    unsatisfail_percent = round(unsatisfail_score / userNum, 4)
    unknown_score = len(Canditate.objects.filter(depart=depart).fitler(cpoint1=1))
    unknown_percent = round(unknown_score / userNum, 4)
    average = round((satisfied_percent * 100 + basical_percent * 60) / (1 - unknown_percent), 4)
    dataDict = {
        "secondDepart": "安太堡露天矿",
        "satisfied_percent": satisfied_percent,
        "basical_percent": basical_percent,
        'unsatisfail_percent': unsatisfail_percent,
        'unknown_percent': unknown_percent,
        "average": average
    }
    datajson = json.dumps(dataDict, cls=DjangoJSONEncoder)
    return HttpResponse(datajson)

# “一报告两评议”结果反馈表七
def feedBackTable7(request):
    depart = 103
    userNum = len(User.objects.filter(depart=depart).filter(ustatus_1=True))
    notExist = len(User.objects.filter(depart=depart).filter(ustatus_1=True).filter(ccheck_=1))
    unknown = len(User.objects.filter(depart=depart).filter(ustatus_1=True).filter(ccheck_=2))
    exist = len(User.objects.filter(depart=depart).filter(ustatus_1=True).filter(ccheck_=0))
    average = round(exist/userNum, 4)
    dataDict = {
        'total': userNum,
        'notExist': notExist,
        'unknown': unknown,
        'exist': exist,
        'average': average
    }
    datajson = json.dumps(dataDict, cls=DjangoJSONEncoder)
    return HttpResponse(datajson)