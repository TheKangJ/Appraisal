from django.db import models

# Create your models here.
'''
UserTypeChoice{
    (1, 'Administrator')
    (2, 'Manager')
    (3, 'User')
}
'''


class Administrator(models.Model):
    user_type = models.IntegerField(default=1, verbose_name='用户类型')
    aname = models.CharField(max_length=30, verbose_name='管理员姓名')  # 管理员姓名
    apasswd = models.CharField(max_length=40, verbose_name='管理员密码')  #
    acreateTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'Administrator'


class Manager(models.Model):  # 二级管理员
    user_type = models.IntegerField(default=2, verbose_name='二级管理员类型')
    mname = models.CharField(max_length=30, verbose_name='二级管理员账号')
    mdepart = models.IntegerField(verbose_name='所属二级部门')
    mcreateTime = models.DateTimeField(
        auto_now_add=True, verbose_name='创建此二级账号时间')

    class Meta:
        db_table = 'Manager'

    @classmethod
    def createManager(cls, type, name, depart, createT):
        magr = cls(
            user_type=type,
            mname=name,
            mdepart=depart,
            mcreateTime=createT)
        return magr



class User(models.Model):
    user_type = models.IntegerField(default=3)
    uname = models.IntegerField(verbose_name='普通平用户ID')
    ucreateTime = models.DateField(auto_now_add=True)
    ustatus_1 = models.BooleanField(verbose_name='填写表1是否完成，默认未完成', default=False)
    ustatus_2 = models.BooleanField(verbose_name='填写表2是否完成，默认为完成', default=False)
    udepart = models.IntegerField(verbose_name='所属二级部门')
    question1 = models.IntegerField(
        verbose_name='对本单位选人用人工作的总体评价', default=0)  # 满意4，基本满意3，不满意2，不了解1
    question2 = models.IntegerField(
        verbose_name='对本单位执行选人用人工作政策法规情况的看法', default=0)  # 满意4，基本满意3，不满意2，不了解1
    question3 = models.IntegerField(
        verbose_name='对本单位整治用人上不正之风工作的看法基本满意', default=0)  # 满意4，基本满意3，不满意2，不了解1
    question4 = models.IntegerField(
        verbose_name='对本单位深化干部人事制度改革的看法满意', default=0)   # 满意4，基本满意3，不满意2，不了解1
    question5_1 = models.IntegerField(
        verbose_name='执行《干部任用条例》规定的资格、条件和程序不严格', default=0)
    question5_2 = models.IntegerField(verbose_name='任人唯亲', default=0)
    question5_3 = models.IntegerField(verbose_name='领导干部用人上个人说了算', default=0)
    question5_4 = models.IntegerField(verbose_name='跑官要官、说情打招呼', default=0)
    question5_5 = models.IntegerField(verbose_name='买官卖官', default=0)
    question5_6 = models.IntegerField(verbose_name='拉票', default=0)
    question5_7 = models.CharField(verbose_name='其他', default='', max_length=200)
    question5_8 = models.IntegerField(verbose_name='不存在突出问题', default=0)
    question6 = models.CharField(verbose_name='单位选人用人工作有何意见', default='', max_length=200)
    class Meta:
        db_table = 'user'
    @classmethod
    def createUser(cls, type, name, ucreateT,depart):
        usr = cls(uname=name, ucreateTime=ucreateT, udepart=depart)
        return usr


class Canditate(models.Model):  # 候选人
    cname = models.CharField(max_length=30, verbose_name='候选人名称')
    cdepart = models.IntegerField()
    cgender = models.CharField(verbose_name='候选人性别', max_length=20)
    cbirth = models.DateField()
    cjobbef = models.CharField(max_length=30, verbose_name='现任职务')  #
    cjobnow = models.CharField(max_length=30, verbose_name='原任职务')  #
    cjobnowT = models.DateField()
    cpoint_4 = models.IntegerField(
        verbose_name='对任用该干部的看法满意',
        default=0)  # ：满意4，基本满意3，不满意2,不了解1
    cpoint_3 = models.IntegerField(verbose_name='对任用该干部的看法基本满意', default=0)
    cpoint_2 = models.IntegerField(verbose_name='对任用该干部的看法不满意', default=0)
    cpoint_1 = models.IntegerField(verbose_name='对任用该干部的看法不了解', default=0)
    ccheck_0 = models.IntegerField(
        verbose_name='是否存在拉票、跑官、买官行为存在',
        default=0)  # :存在3，不了解2，不存在1
    ccheck_1 = models.IntegerField(verbose_name='是否存在拉票、跑官、买官行为不了解', default=0)
    ccheck_2 = models.IntegerField(verbose_name='是否存在拉票、跑官、买官行为不了解', default=0)

    class Meta:
        db_table = 'Canditate'

    @classmethod
    def createCanditate(
            cls,
            name,
            depart,
            gender,
            birth,
            jobnow,
            jobbef,
            jobnowT,
    ):
        candit = cls(
            cname=name,
            cdepart=depart,
            cgender=gender,
            cbirth=birth,
            cjobnow=jobnow,
            cjobbef=jobbef,
            cjobnowT=jobnowT,
        )
        return candit


class Inform(models.Model):  # 通知
    username = models.CharField(max_length=30, verbose_name='用户名')
    informtext = models.TextField()
    createTime = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'inform'

    @classmethod
    def createInform(cls, name, informT, createT):
        info = cls(username=name, informtext=informT, createTime=createT)
        return info
