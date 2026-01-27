"""Views for accounts app."""
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str, smart_str
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, UserSerializer


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """Handle user login."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = force_str(serializer.validated_data['username'])
        password = force_str(serializer.validated_data['password'])

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:
            error_message = _('Invalid credentials')
            return Response(
                {'error': smart_str(error_message)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)
        
        # Return different response format for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return Response({
                'success': True,
                'user': UserSerializer(user).data,
                'message': smart_str(_('Login successful')),
            })
        return Response(UserSerializer(user).data)


class LogoutView(APIView):
    """Handle user logout."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = force_str(request.user.username)
        logout(request)
        
        message = _('Logged out successfully')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return Response({
                'success': True,
                'message': smart_str(message),
                'username': username,
            })
        return Response({'message': smart_str(message)})


class MeView(APIView):
    """Return current user info."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = UserSerializer(request.user).data
        
        # Add extra info for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            user_data['display_name'] = smart_str(
                force_str(request.user.get_full_name()) or 
                force_str(request.user.username)
            )
        return Response(user_data)
