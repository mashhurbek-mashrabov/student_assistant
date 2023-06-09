# Generated by Django 4.2.2 on 2023-06-16 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor_bot', '0005_alter_tutortelegramuser_status'),
        ('student_bot', '0002_alter_studenttelegramuser_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, related_name='membership', to='student_bot.studenttelegramuser')),
                ('status', models.IntegerField(choices=[(1, 'New'), (2, 'Pending'), (3, 'Active'), (4, 'Rejected')], default=1)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='tutor_bot.studentgroup')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
