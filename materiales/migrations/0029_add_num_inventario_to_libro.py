from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0028_programa_fecha_baja_proyector_fecha_baja'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='num_inventario',
            field=models.CharField(max_length=50, blank=True, null=True, default=''),
        ),
    ]