from rest_framework import generics, serializers, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import CreateUserSerializer, LoginUserSerializer, UserSerializer
from .models import User
from .utils import get_user_jwt, error_detail, check_expired_tokens


# registration view
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                data = serializer.validate(data=request.data)
                user = User.objects.create_user(**data)
                user.set_password(data['password'])
                jwt_tokens = get_user_jwt(user)
                return Response({
                        'status': 'success',
                        'detail': "User registered successfully!",
                        'tokens': jwt_tokens
                    })

        except serializers.ValidationError as e:
            data = {
                'status': 'error',
                'detail': error_detail(e)
                }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        

# login view 
class LoginUserView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginUserSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            check_expired_tokens(user)
            jwt_tokens = get_user_jwt(user)
            return Response({
                'status': 'success',
                'detail': "Logged in successfully!",
                'tokens': jwt_tokens
            }, status=status.HTTP_202_ACCEPTED)
        return Response({
            'status': 'error',
            'detail': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
            
            
class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        try:
            user = self.retrieve(request, *args, **kwargs).data
            if user.get('username') == request.user.username:
                return Response({
                            'status': 'success',
                            'owner': True,
                            "user": user,
                        })
            else:
                return Response({
                    'status': 'success',
                    'owner': False,
                    "user": user.get('username'),
                })

        except serializers.ValidationError as e:
            data = {
                'status': 'error',
                'detail': error_detail(e)
                }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        

        

    
 