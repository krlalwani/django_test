from django.db import models
from django.forms import model_to_dict
import pandas as pd

# Create your models here.
class Student(models.Model):
    name = models.CharField()
    email = models.EmailField()
    dob = models.DateField()
    roll = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    
    def convert_df(self) -> pd.DataFrame:   ## convert data records to df
        return pd.DataFrame.from_records(self.values())
    
    def convert_dict(self): #convert single record to dict
        return model_to_dict(self)
    
    class Meta:
        db_table = 'Student' ## provide explicit name of table



class Address(models.Model):
    student = models.ForeignKey(Student,on_delete= models.CASCADE, related_name='addresses') # related_name for reverse relation
    add_line1 = models.CharField()
    city = models.CharField()
    pincode = models.IntegerField()
    class AddrType(models.TextChoices):
        R = 'RESIDENCE'
        P = 'PERMANENT'
        C = 'COMMUNICATION'
    addr_type = models.CharField(choices=AddrType,default=AddrType.R)

    def __str__(self):
        return self.city
    
    def convert_df(self) -> pd.DataFrame:   ## convert data records to df
        address_df = pd.DataFrame.from_records(self.values())
        return address_df
    
    def convert_dict(self): #convert single record to dict
        return model_to_dict(self)

    @classmethod        # making this method static to allow access from outside the class
    def get_enum_value(self,type):
        try:
            return self.AddrType[type].value
        except KeyError:
            return 'RESIDENCE'

    class Meta:
        db_table = 'Address' ## provide explicit name of table