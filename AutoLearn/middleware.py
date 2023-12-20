from django.http import HttpResponse
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.urls import reverse

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.login_url = reverse('login')
        self.register_url = reverse('register')

    def __call__(self, request):
        
        # Replace 'login' with the name or path of your login view
        if request.path == self.login_url or request.path == self.register_url:
            return self.get_response(request)
        
        token = request.COOKIES.get('jwt')

        if not token:
            return HttpResponse("Unauthorised", status=401)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            request.jwt_payload = payload
        
        except jwt.ExpiredSignatureError:
            return HttpResponse("Unauthorised", status=401)

        response = self.get_response(request)
        return response