from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('piso', '0003_auto_20220610_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_puesto', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre puesto de trabajo')),
                ('capacidad_puesto', models.IntegerField(blank=True, default=0, null=True, verbose_name='Capacidad puesto trabajo')),
                ('estado', models.CharField(blank=True, default='Activo', max_length=100, null=True, verbose_name='Estado')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Fecha Actualización')),
                ('piso', models.ForeignKey(on_delete='cascade', to='piso.Piso')),
            ],
            options={
                'verbose_name': 'Puesto',
                'verbose_name_plural': 'Puestos',
                'ordering': ['nombre_puesto'],
            },
        ),
    ]