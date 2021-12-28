from rest_framework.views import APIView

from apps.CustomUser.models import Profile, User
from utils.token_helper import generate_access_token, generate_refresh_token
from .serializers import ProfileSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.parsers import JSONParser

class Login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        response = Response()

        if (username is None) or (password is None):
            raise exceptions.AuthenticationFailed("Username and password required.")

        user = User.objects.filter(username=username).first()
        if user is None:
            raise exceptions.AuthenticationFailed("User not found.")
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Wrong password.")
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
        response.data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return response

class Register(APIView):

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        email = data["email"]
        data["user"] = {
            "username": data["email"].split('@')[0],
            "email": data["email"],
            "password": data["password"],
        }
        print(data["user"])
        try:
            userIns = User.objects.get(email=data["email"])
        except:
            userIns = None
        try:
            profile = Profile.objects.get(email=data["email"])
        except:
            profile = None

        if userIns != None or profile != None:
            raise exceptions.NotAcceptable("Username or Email already in use.")

        serializer2 = ProfileSerializer(data=data)
        
        if serializer2.is_valid():
            serializer2.save()
            user = User.objects.get(email=email)
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)
            return Response({
                "status": "User succesfully created.",
                "access_token": access_token,
                "refresh_token": refresh_token,
            })
        else:
            print(serializer2.errors)
            raise exceptions.ValidationError("User validation Error.")
