# Generated by Django 4.2.15 on 2024-08-20 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reference',
            old_name='entity_name',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='car',
            name='drive_axle_model',
            field=models.ForeignKey(limit_choices_to={'category': 'drive_axle_model'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='car_drive_axle_models', to='cars.reference'),
        ),
        migrations.AlterField(
            model_name='car',
            name='engine_model',
            field=models.ForeignKey(limit_choices_to={'category': 'engine_model'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='car_engine_models', to='cars.reference'),
        ),
        migrations.AlterField(
            model_name='car',
            name='steering_axle_model',
            field=models.ForeignKey(limit_choices_to={'category': 'steering_axle_model'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='car_steering_axle_models', to='cars.reference'),
        ),
        migrations.AlterField(
            model_name='car',
            name='tech_model',
            field=models.ForeignKey(limit_choices_to={'category': 'tech_model'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='car_tech_models', to='cars.reference'),
        ),
        migrations.AlterField(
            model_name='car',
            name='transmission_model',
            field=models.ForeignKey(limit_choices_to={'category': 'transmission_model'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='car_transmission_models', to='cars.reference'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='failure_node',
            field=models.ForeignKey(limit_choices_to={'category': 'failure_node'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='failure_nodes', to='cars.reference'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='recovery_method',
            field=models.ForeignKey(limit_choices_to={'category': 'recovery_method'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recovery_methods', to='cars.reference'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='maintenance_organization',
            field=models.ForeignKey(limit_choices_to={'category': 'maintenance_organization'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintenance_organizations', to='cars.reference'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='maintenance_type',
            field=models.ForeignKey(limit_choices_to={'category': 'maintenance_type'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintenance_types', to='cars.reference'),
        ),
    ]
