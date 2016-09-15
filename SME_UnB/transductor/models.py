from __future__ import unicode_literals

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import ArrayField
from polymorphic.models import PolymorphicModel


class TransductorModel(models.Model):
    """
        Class responsible to define a transductor model which contains crucial informations about the
        transductor itself.

        Attributes:
            - name(str): The factory name.
            - internet_protocol(str): The internet protocol.
            - serial_protocol(str): The serial protocol.
            - register_addresses(list): Registers with data to be collected.
                This attribute must meet the following pattern:

                [[Register Number, Register Type]]

                Where:
                    - Register Address: register address itself.
                    - Register Type: register data type.
                        - 0 - Integer
                        - 1 - Float

                Example: [[68, 0], [70, 1]]

        Example of use:

        >>> TransductorModel(name="Test Name", internet_protocol="UDP", serial_protocol="Modbus RTU", register_addresses=[[68, 0], [70, 1]])
        <TransductorModel: Test Name>
    """
    name = models.CharField(max_length=50, unique=True)
    internet_protocol = models.CharField(max_length=50)
    serial_protocol = models.CharField(max_length=50)
    register_addresses = ArrayField(ArrayField(models.IntegerField()))

    def __str__(self):
        return self.name


class Transductor(models.Model):
    """
        Base class responsible to create an abstraction of a transductor.

        Attributes:
            - model(TransductorModel): The transductor model.
            - serie_number(int): The serie number.
            - ip_address(str): The ip address.
            - description(str): A succint description.
            - creation_date(datetime): The date/time creation.
    """
    model = models.ForeignKey(TransductorModel)
    serie_number = models.IntegerField(default=None)
    ip_address = models.CharField(max_length=15, unique=True, validators=[
        RegexValidator(
            regex='^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$',
            message='Incorrect IP address format',
            code='invalid_ip_address'
        ),
    ])
    description = models.TextField(max_length=150)
    creation_date = models.DateTimeField('date published')

    class Meta:
        abstract = True


class EnergyTransductor(Transductor):
    """
        Class responsible to represent a Energy Transductor which will collect energy measurements.

        Example of use:

        >>> from django.utils import timezone
        >>> t_model = TransductorModel(name="Test Name", internet_protocol="UDP", serial_protocol="Modbus RTU", register_addresses=[[68, 0], [70, 1]])
        >>> EnergyTransductor(model=t_model, serie_number=1, ip_address="1.1.1.1", description="Energy Transductor Test", creation_date=timezone.now())
        <EnergyTransductor: Energy Transductor Test>
    """
    def __str__(self):
        return self.description


class Measurements(PolymorphicModel):

    collection_date = models.DateTimeField('date published')
    collection_minute = models.IntegerField(default=None)


class EnergyMeasurements(Measurements):

    transductor = models.ForeignKey(EnergyTransductor, on_delete=models.CASCADE)

    voltage_a = models.FloatField(default=None)
    voltage_b = models.FloatField(default=None)
    voltage_c = models.FloatField(default=None)

    current_a = models.FloatField(default=None)
    current_b = models.FloatField(default=None)
    current_c = models.FloatField(default=None)

    active_power_a = models.FloatField(default=None)
    active_power_b = models.FloatField(default=None)
    active_power_c = models.FloatField(default=None)

    reactive_power_a = models.FloatField(default=None)
    reactive_power_b = models.FloatField(default=None)
    reactive_power_c = models.FloatField(default=None)

    apparent_power_a = models.FloatField(default=None)
    apparent_power_b = models.FloatField(default=None)
    apparent_power_c = models.FloatField(default=None)

    def __str__(self):
        return '%s' % self.collection_date

    def calculate_total_active_power(self):
        return (self.active_power_a + self.active_power_b + self.active_power_c)

    def calculate_total_reactive_power(self):
        return (self.reactive_power_a + self.reactive_power_b + self.reactive_power_c)

    def calculate_total_apparent_power(self):
        ap_phase_a = self.apparent_power_a
        ap_phase_b = self.apparent_power_b
        ap_phase_c = self.apparent_power_c

        ap_total = (ap_phase_a + ap_phase_b + ap_phase_c)

        return ap_total
