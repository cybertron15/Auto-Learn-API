from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import User, CourseInfo, UserCourseInfo, Topic, ChatIdTable, ChatInfo
from .forms import CourseForm
from django.http import request
from django.http import JsonResponse
from django.core.serializers import serialize
# # Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
# from datetime import datetime
from course_content.new import content_def
import json
from rest_framework.views import APIView, Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, CourseInfoseriaizer, UserCourseInfoseriaizer, Topicserializer, Topicdataserializer, ChatInfoSerializer
from rest_framework.exceptions import AuthenticationFailed
# Create your views here.
from datetime import datetime, timedelta
import jwt
from django.db.models import Subquery



class RegisterUser(APIView):
    def post(self, request):
        serializer= UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    

class LoginUserView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User Not Found")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")
        
        payload={
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'iat': datetime.utcnow()
        }
        
        token =jwt.encode(payload, "secret", algorithm ='HS256')
        
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        
        response.data = {
                'jwt': f"{token}",
            }
        return response
    
@api_view(['POST'])
def getUser(request):
    user_id = request.jwt_payload['id']
    user=User.objects.filter(id = user_id).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def logoutview(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'success'
    }
    return response


@csrf_exempt
@api_view(['POST'])
def getcourseform(request):
    user_id = request.jwt_payload['id']
    course_name = request.data['course']
    course_level = request.data['level_info']
    

    if CourseInfo.objects.filter(course = course_name, level_info = course_level).exists():
        course_info = get_object_or_404(CourseInfo, course = course_name, level_info = course_level)
        user = get_object_or_404(User, id=user_id)
        
        if UserCourseInfo.objects.filter(Id = user, courseid = course_info).exists():
            new_user_course = UserCourseInfo.objects.filter(Id = user, courseid = course_info)

        
        else: 
            new_user_course = UserCourseInfo.objects.create(Id = user, courseid = course_info)
            tcontent = json.loads(content_def())
            for i, k in tcontent.items():
                topicentry = Topic.objects.create(courseid = course_info.courseid, content=k, tname=i)
                user_topic_chat = ChatIdTable.objects.create(UID = new_user_course.UID, topicid = topicentry.topicid)
                
                chatinfo = ChatInfo.objects.create(chat_id = user_topic_chat.chat_id, chat_q = "Welcome To Learnx", time= datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    else:
        course_info = CourseInfo.objects.create(course=course_name, level_info=course_level)
        user = get_object_or_404(User, id=user_id)
        new_user_course = UserCourseInfo.objects.create(Id = user, courseid = course_info)
        
        tcontent = json.loads(content_def())
        for i, k in tcontent.items():
            topicentry = Topic.objects.create(courseid = course_info.courseid, content=k, tname=i)
            user_topic_chat = ChatIdTable.objects.create(UID = new_user_course.UID, topicid = topicentry.topicid)
            chatinfo = ChatInfo.objects.create(chat_id = user_topic_chat.chat_id, chat_q = "Welcome To Learnx", time= datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
    
    course_seriaizer = CourseInfoseriaizer(course_info)
    return Response(course_seriaizer.data)



@csrf_exempt
@api_view(['POST'])
def getusercourses(request):
    user_id = request.jwt_payload['id']
    user = get_object_or_404(User, id=user_id)
    all_ids = UserCourseInfo.objects.filter(Id=user).values('courseid')
    courseinfo_obj=CourseInfo.objects.filter(courseid__in = Subquery(all_ids))
    
    
    return Response(CourseInfoseriaizer(courseinfo_obj, many=True).data)
    

@csrf_exempt
@api_view(['POST'])
def getcoursetopics(request):
    course_id=request.data['courseid']
    return Response(Topicserializer(Topic.objects.filter(courseid= course_id),many=True).data)
    
@csrf_exempt
@api_view(['POST'])
def contentandchats(request):
    # user_id = payload['id']
    user_id = request.jwt_payload['id']
    topic_id = request.data['topicid']
    courseid = Topic.objects.filter(topicid=topic_id).values('courseid')[0]['courseid']
    uid = UserCourseInfo.objects.filter(Id=user_id, courseid=courseid).values('UID')[0]['UID']

    topic_content = Topicdataserializer(Topic.objects.filter(topicid=topic_id), many=True)
    
    chat_d = ChatIdTable.objects.filter(UID=uid, topicid=topic_id).values('chat_id')[0]['chat_id']
    chat_content = ChatInfo.objects.filter(chat_id = chat_d)
    
    combined_data = {
        'chat_info': ChatInfoSerializer(chat_content, many=True).data,
        'topic_data': topic_content.data,
    }
    return Response(combined_data)


@csrf_exempt
@api_view(['POST'])
def processchat(request):
    user_id = request.jwt_payload['id']
    topic_id = request.data['topicid']
    chatcontent = request.data['chatcontent']
    courseid = Topic.objects.filter(topicid=topic_id).values('courseid')[0]['courseid']
    uid = UserCourseInfo.objects.filter(Id=user_id, courseid=courseid).values('UID')[0]['UID']
    chat_d = ChatIdTable.objects.filter(UID=uid, topicid=topic_id).values('chat_id')[0]['chat_id']
    
    if chatcontent.split(":")[0]=="Notes" or chatcontent.split(":")[0]=="notes" or chatcontent.split(":")[0]=="Note":
        chat_content = ChatInfo.objects.create(chat_id = chat_d, chat_notes= chatcontent, time= datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    else:
        # generate ans of question
        chat_A= "Yes. Python is compiled language."
        chat_content = ChatInfo.objects.create(chat_id = chat_d, chat_q= chatcontent, chat_A= chat_A, time= datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
   
    return Response("Success")



