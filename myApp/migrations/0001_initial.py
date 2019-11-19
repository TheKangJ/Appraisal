# Generated by Django 2.2.6 on 2019-11-15 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(default=1, verbose_name='用户类型')),
                ('aname', models.CharField(max_length=30, verbose_name='管理员姓名')),
                ('apasswd', models.CharField(max_length=40, verbose_name='管理员密码')),
                ('acreateTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'Administrator',
            },
        ),
        migrations.CreateModel(
            name='Canditate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=30, verbose_name='候选人名称')),
                ('cdepart', models.IntegerField()),
                ('cgender', models.CharField(max_length=20, verbose_name='候选人性别')),
                ('cbirth', models.DateField()),
                ('cjobbef', models.CharField(max_length=30, verbose_name='现任职务')),
                ('cjobnow', models.CharField(max_length=30, verbose_name='原任职务')),
                ('cjobnowT', models.DateField()),
                ('cpoint_4', models.IntegerField(default=0, verbose_name='对任用该干部的看法满意')),
                ('cpoint_3', models.IntegerField(default=0, verbose_name='对任用该干部的看法基本满意')),
                ('cpoint_2', models.IntegerField(default=0, verbose_name='对任用该干部的看法不满意')),
                ('cpoint_1', models.IntegerField(default=0, verbose_name='对任用该干部的看法不了解')),
                ('ccheck_0', models.IntegerField(default=0, verbose_name='是否存在拉票、跑官、买官行为存在')),
                ('ccheck_1', models.IntegerField(default=0, verbose_name='是否存在拉票、跑官、买官行为不了解')),
                ('ccheck_2', models.IntegerField(default=0, verbose_name='是否存在拉票、跑官、买官行为不了解')),
            ],
            options={
                'db_table': 'Canditate',
            },
        ),
        migrations.CreateModel(
            name='Inform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, verbose_name='用户名')),
                ('informtext', models.TextField()),
                ('createTime', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'inform',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(default=2, verbose_name='二级管理员类型')),
                ('mname', models.CharField(max_length=30, verbose_name='二级管理员账号')),
                ('mdepart', models.IntegerField(verbose_name='所属二级部门')),
                ('mcreateTime', models.DateTimeField(auto_now_add=True, verbose_name='创建此二级账号时间')),
            ],
            options={
                'db_table': 'Manager',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(default=3)),
                ('uname', models.IntegerField(verbose_name='普通平用户ID')),
                ('ucreateTime', models.DateField(auto_now_add=True)),
                ('ustatus_1', models.BooleanField(default=False, verbose_name='填写表1是否完成')),
                ('ustatus_2', models.BooleanField(default=False, verbose_name='填写表2是否完成')),
                ('udepart', models.IntegerField(verbose_name='所属二级部门')),
                ('question1', models.IntegerField(default=0, verbose_name='对本单位选人用人工作的总体评价')),
                ('question2', models.IntegerField(default=0, verbose_name='对本单位执行选人用人工作政策法规情况的看法')),
                ('question3', models.IntegerField(default=0, verbose_name='对本单位整治用人上不正之风工作的看法基本满意')),
                ('question4', models.IntegerField(default=0, verbose_name='对本单位深化干部人事制度改革的看法满意')),
                ('question5_1', models.IntegerField(default=0, verbose_name='执行《干部任用条例》规定的资格、条件和程序不严格')),
                ('question5_2', models.IntegerField(default=0, verbose_name='任人唯亲')),
                ('question5_3', models.IntegerField(default=0, verbose_name='领导干部用人上个人说了算')),
                ('question5_4', models.IntegerField(default=0, verbose_name='跑官要官、说情打招呼')),
                ('question5_5', models.IntegerField(default=0, verbose_name='买官卖官')),
                ('question5_6', models.IntegerField(default=0, verbose_name='拉票')),
                ('question5_7', models.CharField(default='', max_length=200, verbose_name='其他')),
                ('question5_8', models.IntegerField(default=0, verbose_name='不存在突出问题')),
                ('question6', models.CharField(default='', max_length=200, verbose_name='单位选人用人工作有何意见')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]