from django.db import models
from django.contrib.auth.models import AbstractUser
#from slot_machine_app.models import Player, SpinResult

class userInfo(models.Model) :
    UID = models.IntegerField(db_column='UID',primary_key=True)
    AUTH_ID = models.IntegerField(db_column='AUTH_ID',default=3)
    PASSWORD = models.CharField(db_column='PASSWORD',max_length=30)
    NICK = models.CharField(db_column='NICK',max_length=30)
    EMAIL = models.CharField(db_column='EMAIL',max_length=128)
    MONEY = models.IntegerField(db_column='MONEY',default=50000)
    LOGIN_ID = models.CharField(db_column='LOGIN_ID',max_length=32)
    
    class Meta :
        managed = False
        db_table = 'userInfo'
        
    def __str__(self) :
        return self.NICK
    

# Create your models here.
