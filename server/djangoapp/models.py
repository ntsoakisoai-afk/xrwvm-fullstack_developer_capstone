from django.db import models


class CarMake(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField()

    def __str__(self):
        return self.name


class CarModel(models.Model):

    CAR_TYPE = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Wagon', 'Wagon'),
    )

    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE
    )

    dealer_id = models.IntegerField()

    name = models.CharField(
        max_length=100
    )

    car_type = models.CharField(
        max_length=20,
        choices=CAR_TYPE,
        default='Sedan'
    )

    year = models.IntegerField()

    def __str__(self):
        return self.car_make.name + " : " + self.name