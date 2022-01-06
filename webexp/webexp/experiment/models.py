from django.db import models


class Participant(models.Model):
    participant_id = models.CharField(max_length=50)
    charity = models.CharField(max_length=50, default="NA")
    reward = models.CharField(max_length=10, default="NA")
    charity_reward = models.CharField(max_length=10, default="NA")
    bank_account = models.CharField(max_length=50, default="NA")
    status = models.CharField(max_length=50, default="NA")
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now=True)

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields(): # pylint: disable=no-member
            field_values.append(str(getattr(self, field.name, '')))
        return '\t'.join(field_values)


class Trial(models.Model):
    participant_id = models.CharField(max_length=50)
    order = models.CharField(max_length=3)	
    time_screen = models.CharField(max_length=50)	
    shape = models.CharField(max_length=10)	
    color = models.CharField(max_length=10)	
    bribe = models.CharField(max_length=6)	
    response_shape = models.CharField(max_length=10)	
    response_color = models.CharField(max_length=10)	
    correct_shape = models.CharField(max_length=10)	
    correct_color = models.CharField(max_length=10)	
    charity_total = models.CharField(max_length=6)
    reward_total = models.CharField(max_length=6)	
    response_number = models.CharField(max_length=1)		
    color1 = models.CharField(max_length=10)	
    color2 = models.CharField(max_length=10)	
    color3 = models.CharField(max_length=10)	
    shape1 = models.CharField(max_length=10)	
    shape2 = models.CharField(max_length=10)	
    shape3 = models.CharField(max_length=10)
    condition = models.CharField(max_length=12, default="NA")

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields(): # pylint: disable=no-member
            field_values.append(str(getattr(self, field.name, '')))
        return '\t'.join(field_values)


class Code(models.Model):
    code = models.CharField(max_length=36)
    page = models.IntegerField(default=0)

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields(): # pylint: disable=no-member
            field_values.append(str(getattr(self, field.name, '')))
        return '\t'.join(field_values)


class Log(models.Model):
    code = models.CharField(max_length=36)
    page = models.IntegerField()
    request = models.CharField(max_length=4)
    time = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=8, default="error")

    def __str__(self):
        field_values = []
        for field in self._meta.get_fields(): # pylint: disable=no-member
            field_values.append(str(getattr(self, field.name, '')))
        return '\t'.join(field_values)