# Generated by Django 4.1.7 on 2023-06-04 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick_name', models.CharField(max_length=50, verbose_name='昵称')),
                ('gender', models.CharField(choices=[('m', '男'), ('f', '女')], default='m', max_length=10, verbose_name='性别')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('admin_number', models.CharField(max_length=20, verbose_name='账号')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick_name', models.CharField(max_length=50, verbose_name='昵称')),
                ('gender', models.CharField(choices=[('m', '男'), ('f', '女')], default='m', max_length=10, verbose_name='性别')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('client_number', models.CharField(max_length=20, verbose_name='账号')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
            ],
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('client_number',), name='client_number'),
        ),
        migrations.AddConstraint(
            model_name='admin',
            constraint=models.UniqueConstraint(fields=('admin_number',), name='admin_number'),
        ),
    ]
