"""Views for accounts app."""
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text, smart_text
from django.utils.translation import ugettext as _
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

        username = force_text(serializer.validated_data['username'])
        password = force_text(serializer.validated_data['password'])

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:
            error_message = _(u'Invalid credentials')
            return Response(
                {'error': smart_text(error_message)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)
        
        # Return different response format for AJAX requests
        if request.is_ajax():
            return Response({
                'success': True,
                'user': UserSerializer(user).data,
                'message': smart_text(_(u'Login successful')),
            })
        return Response(UserSerializer(user).data)


class LogoutView(APIView):
    """Handle user logout."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = force_text(request.user.username)
        logout(request)
        
        message = _(u'Logged out successfully')
        if request.is_ajax():
            return Response({
                'success': True,
                'message': smart_text(message),
                'username': username,
            })
        return Response({'message': smart_text(message)})


class MeView(APIView):
    """Return current user info."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = UserSerializer(request.user).data
        
        # Add extra info for AJAX requests
        if request.is_ajax():
            user_data['display_name'] = smart_text(
                force_text(request.user.get_full_name()) or 
                force_text(request.user.username)
            )
        return Response(user_data)
