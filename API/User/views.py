from django.http.response import JsonResponse
from rest_framework import status
from API.models import *
from API.serializers import *
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from SmartHomeAPI import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import request
from ..views import SmartHomeAuthView


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()

            return JsonResponse({
                'message': 'Register successful!'
            }, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({
                'error_message': 'This phone number has already exist!',
                'errors_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['phone_number'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                    'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                    'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
                }
                # save into database
                
                #
                return Response(data, status=status.HTTP_200_OK)

            return Response({
                'error_message': 'phone number or password is incorrect!',
                'error_code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(SmartHomeAuthView):
    def post(self, request):
        if request.data and request.data["password"] and request.data["old_password"]:
            username = self.request.user.phone_number
            users = User.objects.filter(phone_number=username)
            if users:
                user = users.first()
                if not user.check_password(request.data["old_password"]):
                    return Response(status=status.HTTP_400_BAD_REQUEST, data="Wrong password")
                user.password = make_password(request.data["password"])
                user.save()
                return Response(status=status.HTTP_200_OK, data="Password changed")
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Can't seem to find that user in the database")
        return Response(status=status.HTTP_400_BAD_REQUEST, data="Possibly wrong data format")

class TestAuth(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request:request.Request):
        print(self.request.user.password)
        content = {'message': 'Hello, ' + self.request.user.phone_number}
        return Response(content)