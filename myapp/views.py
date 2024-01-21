from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, permissions, authentication, pagination, response, decorators, status
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, UserSerializer
from django.shortcuts import get_object_or_404



@decorators.api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = get_object_or_404(User, username=username)
    if not user.check_password(password):
        return response.Response({'error': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    return response.Response({'token': token.key, 'user': UserSerializer(user).data})


@decorators.api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        if User.objects.filter(username=username).exists():
            return response.Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return response.Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return response.Response({'token': token.key, 'user': serializer.data})
    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@decorators.api_view(['GET'])
def logout(request):
    request.user.auth_token.delete()
    return response.Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        
class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return response.Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'page_size': self.page_size,
            'data': data
        })

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        queryset = Post.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(author=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
