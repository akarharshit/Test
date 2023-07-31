from django.shortcuts import render

# Create your views here.
# user_roles_app/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import UserProfile, UserPermission
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes



@csrf_exempt

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        if username and password and role:
            user = User.objects.create_user(username=username, password=password)
            if role == 'admin':
                user.is_superuser = True
                user.is_staff = True
            user.save()

            # Generate and return JWT token for the registered user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return JsonResponse({'message': 'User registered successfully', 'access_token': access_token})
        else:
            return JsonResponse({'error': 'Please provide all required form data'}, status=400)
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)



@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, JWTAuthentication])  # Include JWTAuthentication
@permission_classes([IsAuthenticated])
def profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        profile.save()

    if request.method == 'POST' and request.FILES.get('image'):
        profile.image = request.FILES['image']
        profile.save()

    return render(request, 'profile.html', {'profile': profile})




from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import JsonResponses

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def grant_permission(request):
    normal_users = User.objects.filter(is_superuser=False, is_staff=False)
    if not normal_users.exists():
        return JsonResponse({'message': 'No normal users found.'}, status=404)

    random_user = normal_users.order_by('?').first()
    permission = UserPermission(admin=request.user, normal_user=random_user, permission_granted=True)
    permission.save()

    return JsonResponse({'message': 'Permission granted to a random normal user.', 'username': random_user.username}, status=200)
