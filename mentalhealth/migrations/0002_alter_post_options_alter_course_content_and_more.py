# Generated by Django 4.2.11 on 2024-07-24 09:32

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):
    dependencies = [
        ("mentalhealth", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"verbose_name": "發佈文章", "verbose_name_plural": "發佈文章"},
        ),
        migrations.AlterField(
            model_name="course",
            name="content",
            field=mdeditor.fields.MDTextField(verbose_name="内容"),
        ),
        migrations.AlterField(
            model_name="post",
            name="content",
            field=mdeditor.fields.MDTextField(verbose_name="内容"),
        ),
    ]