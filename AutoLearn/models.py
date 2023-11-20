from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=600)
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
        
class CourseInfo(models.Model):
    course = models.CharField(max_length=50)
    level_info = models.CharField(max_length=50)
    courseid = models.BigAutoField(primary_key=True)
    
    class Meta:
        managed = True
        db_table = 'courseinfo'
            
class UserCourseInfo(models.Model):
    UID = models.BigAutoField(primary_key = True)
    Id = models.ForeignKey(User, on_delete = models.CASCADE, db_column= 'id')
    courseid = models.ForeignKey(CourseInfo, on_delete = models.CASCADE, db_column = 'courseid')
    
    class Meta:
        managed = True
        db_table = 'usercourseinfo'
        
class Topic(models.Model):
    topicid = models.BigAutoField(primary_key=True)
    courseid = models.IntegerField()
    content = models.TextField()
    tname = models.CharField(max_length=50)
    
    class Meta:
        managed = True
        db_table = 'topic'
        
        
class ChatIdTable(models.Model):
    chat_id = models.BigAutoField(primary_key=True)
    UID = models.IntegerField()
    topicid = models.IntegerField()
    
    class Meta:
        managed = True
        db_table = 'chatidtable'
        
class ChatInfo(models.Model):
    chatinfo_id=models.BigAutoField(primary_key=True)
    chat_id = models.IntegerField()
    chat_q = models.TextField()
    chat_A = models.TextField()
    chat_notes = models.TextField()
    time= models.DateTimeField()
    
    class Meta:
        managed = True
        db_table = 'chatinfo'
    