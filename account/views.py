from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from .renderers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

#Generating Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistrationView(APIView):
    
    def post(self, request, format= None):
        serializer_class = UserRegistrationSerializer(data=request.data)

        if serializer_class.is_valid(raise_exception=True):
            user = serializer_class.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': "Your Registration Completed"}, status = status.HTTP_201_CREATED)


class UserLoginView(APIView):
    renderer_classes  =[UserRenderer]
    def post(self, request, format= None):
        serializer_class = UserLoginSerializer(data=request.data)

        if serializer_class.is_valid(raise_exception=True):
            email = serializer_class.data.get('email')
            password = serializer_class.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': "Login Success"}, status = status.HTTP_200_OK)
            else:
                return Response({'errors': {"non_field_errors": ['email or password is nor valid.']}}, status = status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes  =[UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format= None):
        serializer_class = UserProfileSerializer(request.user)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

class UserPasswordChangeView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format= None):
        serializer_class = UserPasswordChangeSerializer(data = request.data, context={'user': request.user})

        if serializer_class.is_valid(raise_exception=True):
             return Response({'msg': 'Your password is changed sucessfully'}, status=status.HTTP_200_OK)

class EmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format = None):
        serializer = EmailSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            return Response({'msg': "Reset Email has been sent to your email. Please check it."}, status = status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format = None):
        serializer_class = PasswordResetSerializer(data=request.data, context= {'uid': uid, 'token' : token})
        if serializer_class.is_valid(raise_exception=True):
            return Response("Your Password is reseted sucessfully..", status=status.HTTP_200_OK)
