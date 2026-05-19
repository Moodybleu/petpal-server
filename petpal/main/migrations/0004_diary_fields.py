from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_health_daily_appointments'),
    ]

    operations = [
        migrations.AddField(
            model_name='health',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='health',
            name='visit_type',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='health',
            name='pet_weight',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='health',
            name='shots',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='health',
            name='meds',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='health',
            name='tx_plan',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='daily',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='daily',
            name='log_type',
            field=models.CharField(blank=True, default='general', max_length=50),
        ),
        migrations.AddField(
            model_name='daily',
            name='details',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='appointments',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointments',
            name='title',
            field=models.CharField(blank=True, default='Appointment', max_length=100),
        ),
    ]
