# Generated by Django 4.1.1 on 2023-05-16 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LearnmateEdu', '0011_table_quiz_quizresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizresult',
            name='percent',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
        ),
    ]
