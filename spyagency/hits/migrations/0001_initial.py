# Generated by Django 3.2.6 on 2021-09-06 21:57

from django.db import migrations, models
import simple_history.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalHit',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('transaction_id', models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='UUID', null=True, verbose_name='Identificador')),
                ('pub_date', models.DateTimeField(blank=True, editable=False, help_text='DateTime', verbose_name='Fecha de Creación')),
                ('mod_date', models.DateTimeField(blank=True, editable=False, help_text='DateTime', verbose_name='Fecha de modificación')),
                ('is_active', models.BooleanField(default=True, help_text='Boolean', verbose_name='¿Activo?')),
                ('code_hit', models.CharField(editable=False, help_text='varchar(100) *', max_length=100, verbose_name='Código')),
                ('status', models.SmallIntegerField(choices=[(1, 'Activo'), (2, 'Finalizado'), (3, 'Fallido')], default=1, verbose_name='Status del hit')),
                ('level', models.SmallIntegerField(choices=[(1, 'Fácil'), (2, 'Intermedio'), (3, 'Difícil')], default=3, verbose_name='Level del hit')),
                ('hit_detail', models.TextField(blank=True, help_text='text no required', null=True, verbose_name='Detalles del hit')),
                ('status_detail', models.TextField(blank=True, help_text='text no required', null=True, verbose_name='Detalles del status')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical hit',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalTarget',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('transaction_id', models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='UUID', null=True, verbose_name='Identificador')),
                ('pub_date', models.DateTimeField(blank=True, editable=False, help_text='DateTime', verbose_name='Fecha de Creación')),
                ('mod_date', models.DateTimeField(blank=True, editable=False, help_text='DateTime', verbose_name='Fecha de modificación')),
                ('is_active', models.BooleanField(default=True, help_text='Boolean', verbose_name='¿Activo?')),
                ('first_name', models.CharField(help_text='varchar(60) required*', max_length=60, verbose_name='Nombre')),
                ('last_name', models.CharField(help_text='varchar(60) required*', max_length=60, verbose_name='Apellido')),
                ('extra_info', models.JSONField(blank=True, help_text='json no required', null=True, verbose_name='Información adicional')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical target',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='UUID', null=True, verbose_name='Identificador')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='DateTime', verbose_name='Fecha de Creación')),
                ('mod_date', models.DateTimeField(auto_now=True, help_text='DateTime', verbose_name='Fecha de modificación')),
                ('is_active', models.BooleanField(default=True, help_text='Boolean', verbose_name='¿Activo?')),
                ('code_hit', models.CharField(editable=False, help_text='varchar(100) *', max_length=100, verbose_name='Código')),
                ('status', models.SmallIntegerField(choices=[(1, 'Activo'), (2, 'Finalizado'), (3, 'Fallido')], default=1, verbose_name='Status del hit')),
                ('level', models.SmallIntegerField(choices=[(1, 'Fácil'), (2, 'Intermedio'), (3, 'Difícil')], default=3, verbose_name='Level del hit')),
                ('hit_detail', models.TextField(blank=True, help_text='text no required', null=True, verbose_name='Detalles del hit')),
                ('status_detail', models.TextField(blank=True, help_text='text no required', null=True, verbose_name='Detalles del status')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.UUIDField(blank=True, db_index=True, default=uuid.uuid4, editable=False, help_text='UUID', null=True, verbose_name='Identificador')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='DateTime', verbose_name='Fecha de Creación')),
                ('mod_date', models.DateTimeField(auto_now=True, help_text='DateTime', verbose_name='Fecha de modificación')),
                ('is_active', models.BooleanField(default=True, help_text='Boolean', verbose_name='¿Activo?')),
                ('first_name', models.CharField(help_text='varchar(60) required*', max_length=60, verbose_name='Nombre')),
                ('last_name', models.CharField(help_text='varchar(60) required*', max_length=60, verbose_name='Apellido')),
                ('extra_info', models.JSONField(blank=True, help_text='json no required', null=True, verbose_name='Información adicional')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
    ]
