from django.db import models
from django.core.validators import validate_email
from datetime import datetime, date

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self,post_data):
        errors = {}
        if len(post_data["first_name"]) < 3:
            errors["first_name"] = "Please enter more than 2 characters for First Name!"
        if len(post_data["last_name"]) < 3:
            errors["last_name"] = "Please enter more than 2 characters for Last Name!"
        try:
            validate_email(post_data["email"])
        except:
            errors["email"] = "Please enter a valid email!"
        if len(post_data["password"]) < 9:
            errors["password"] = "Please enter at least 8 characters for Password!"
        
        if post_data["password"] != post_data["pw_confirm"]:
            errors["pw_confirm"] = "Please ensure the password matched for confirmation"
        
        if len(post_data["birthday"]) >0 and datetime.strptime(post_data["birthday"], '%Y-%m-%d')> datetime.today():
            errors["birthday"] = "Please enter the date in the past!"
        if len(post_data["birthday"]) >0 and (datetime.strptime(post_data["birthday"], '%Y-%m-%d') - datetime.today())>13:
            errors["birthday"] = "You must be 13 years old to register!"

        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=64)
    birthday = models.DateField(default="2000-10-10")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()