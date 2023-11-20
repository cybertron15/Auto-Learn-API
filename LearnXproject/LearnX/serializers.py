from rest_framework import serializers
from LearnX.models import User, CourseInfo, UserCourseInfo, Topic, ChatInfo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs={
            'password': {'write_only':True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class CourseInfoseriaizer(serializers.ModelSerializer):
    class Meta:
        model = CourseInfo
        fields = ['courseid', 'course', 'level_info']
        
class UserCourseInfoseriaizer(serializers.ModelSerializer):
    class Meta:
        model = UserCourseInfo
        fields = ['UID', 'ID', 'courseid']
        
class Topicserializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['topicid', 'courseid', 'tname']

class Topicdataserializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['topicid', 'content', 'tname']
        
        
class ChatInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatInfo
        fields = ['chat_id', 'chat_q', 'chat_A', 'chat_notes', 'time']
        