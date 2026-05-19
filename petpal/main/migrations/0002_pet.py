from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('breed', models.CharField(max_length=50)),
                ('age', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50)),
                ('catchphrase', models.CharField(max_length=250)),
            ],
        ),
    ]
