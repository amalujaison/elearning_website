# Generated by Django 4.1.1 on 2023-05-11 06:43

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import oscrypto._ffi


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_profile', models.ImageField(upload_to='images')),
                ('name', models.CharField(max_length=200, null=True)),
                ('profession', models.CharField(max_length=200, null=True)),
                ('about_author', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='company_log',
            fields=[
                ('email', models.EmailField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('password', models.TextField(max_length=30)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=200, unique=True)),
                ('image', models.ImageField(upload_to='images')),
                ('price', models.IntegerField()),
                ('description', models.TextField(max_length=500)),
                ('level', models.CharField(max_length=20)),
                ('language', models.CharField(max_length=30)),
                ('students', models.IntegerField()),
                ('slug', models.SlugField(blank=True, default='', max_length=500, null=True)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.category')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=200, unique=True)),
                ('job_image', models.ImageField(upload_to='media/images')),
                ('job_salary', models.IntegerField(default=0)),
                ('job_type', models.CharField(max_length=20)),
                ('job_location', models.CharField(max_length=10)),
                ('slug', models.SlugField(blank=True, default='', max_length=500, null=True)),
                ('job_date', models.DateField(auto_now=True)),
                ('job_description', models.CharField(default=oscrypto._ffi.null, max_length=300)),
                ('job_responsibility', models.CharField(default=oscrypto._ffi.null, max_length=300)),
                ('job_qualifications', models.CharField(default=oscrypto._ffi.null, max_length=300)),
                ('applicant_name', models.CharField(default=oscrypto._ffi.null, max_length=50)),
                ('applicant_email', models.EmailField(default=oscrypto._ffi.null, max_length=30)),
                ('resume', models.FileField(default=oscrypto._ffi.null, upload_to='media/resumes/')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.course')),
            ],
        ),
        migrations.CreateModel(
            name='Reg_Mentor',
            fields=[
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('password', models.TextField(max_length=30)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_user', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='user_log',
            fields=[
                ('email', models.EmailField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('password', models.TextField(max_length=30)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.IntegerField(null=True)),
                ('thumbnail', models.ImageField(null=True, upload_to='media')),
                ('title', models.CharField(max_length=100)),
                ('youtube_id', models.CharField(max_length=200)),
                ('time_duration', models.IntegerField(null=True)),
                ('preview', models.BooleanField(default=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.course')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('password', models.TextField(max_length=30)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_user', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='what_you_learn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.CharField(max_length=500)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.course')),
            ],
        ),
        migrations.CreateModel(
            name='VideoProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watched', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.video')),
            ],
        ),
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watched', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.video')),
            ],
        ),
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('review', models.CharField(blank=True, max_length=500)),
                ('stars', models.CharField(max_length=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='requirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.CharField(max_length=500)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.course')),
            ],
        ),
        migrations.CreateModel(
            name='Reg_company',
            fields=[
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('company_name', models.CharField(blank=True, max_length=50, null=True)),
                ('company_email', models.EmailField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('password', models.CharField(default=True, max_length=100)),
                ('company_phone', models.TextField(max_length=30)),
                ('company_address', models.CharField(max_length=100)),
                ('company_country', models.CharField(max_length=20)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_user', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default='', max_length=50)),
                ('payment_id', models.CharField(default='', max_length=50)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.BooleanField(default=False)),
                ('course', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.course')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.usercourse')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(default=0, max_length=100)),
                ('amount', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('course', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('mentor_name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('category', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.category')),
            ],
        ),
        migrations.CreateModel(
            name='CourseMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='media/coursematerials/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='completed_by',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='mentor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.author'),
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_On', models.DateTimeField(auto_now_add=True)),
                ('certificate_image', models.ImageField(upload_to='certificates/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(blank=True, max_length=500)),
                ('purchase', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('price', models.IntegerField(default=0)),
                ('image', models.ImageField(null=True, upload_to='images')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LearnmateEdu.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
