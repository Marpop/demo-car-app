from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cars", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="car",
            constraint=models.UniqueConstraint(
                fields=("maker", "model"), name="unique name"
            ),
        ),
    ]
