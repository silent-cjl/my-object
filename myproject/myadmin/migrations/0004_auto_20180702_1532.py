# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-02 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0003_auto_20180627_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=20)),
                ('xiangxi', models.CharField(max_length=50)),
                ('status', models.IntegerField(default=0)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Users')),
            ],
            options={
                'db_table': 'adress',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField()),
                ('gid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Goods')),
            ],
            options={
                'db_table': 'orderinfo',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalprice', models.FloatField()),
                ('totalnum', models.IntegerField()),
                ('status', models.IntegerField(default=0)),
                ('addtime', models.DateTimeField(auto_now_add=True, null=True)),
                ('addressid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Address')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Users')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.AddField(
            model_name='orderinfo',
            name='orderid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Orders'),
        ),
    ]