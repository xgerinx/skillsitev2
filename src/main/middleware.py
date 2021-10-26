from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


ACCESS_TOKEN_NAME_in = 'HTTP_AUTHORIZATION'
REFRESH_TOKEN_NAME_in = 'HTTP_REFRESH_TOKEN'

ACCESS_TOKEN_NAME_out = 'HTTP-AUTHORIZATION'
REFRESH_TOKEN_NAME_out = 'HTTP-REFRESH-TOKEN'


class JWTAuthMiddleware:
    """Middleware class responsible for JWT token authentication"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Update refresh and access tokens, if refresh token is valid.
        Add new tokens in request and response headers.
        """
        access = request.META.get(ACCESS_TOKEN_NAME_in, '')
        refresh = request.META.get(REFRESH_TOKEN_NAME_in, '')
        if not refresh:
            request.META[ACCESS_TOKEN_NAME_in] = ''
            return self.tokens_absent_or_invalid(request)

        try:
            auth = AccessToken(access)
            if auth:
                return self.access_token_valid(request, access=access, refresh=refresh)
            else:
                return self.refresh_token_valid(request, access=access, refresh=refresh)

        except (InvalidToken, TokenError):
            return self.refresh_token_valid(request, access=access, refresh=refresh)

    def access_token_valid(self, request, access='', refresh=''):
        """
        Add the same tokens to response headers that was received in request.
        Used when access token is valid
        """
        assert access
        assert refresh

        response = self.get_response(request)
        response[REFRESH_TOKEN_NAME_out] = refresh
        response[ACCESS_TOKEN_NAME_out] = access
        return response

    def refresh_token_valid(self, request, access='', refresh=''):
        """
        Add new tokens to response headers.
        Used when access token has expired and refresh token hasn't.
        """
        try:
            if not access:
                refresh = RefreshToken(refresh)
                # update refresh token
                refresh.set_jti()
                refresh.set_exp()
            else:
                refresh = RefreshToken(refresh)
        except TokenError:
            return self.tokens_absent_or_invalid(request)

        request.META[ACCESS_TOKEN_NAME_in] = f'Bearer {refresh.access_token}'
        response = self.get_response(request)
        response[REFRESH_TOKEN_NAME_out] = str(refresh)
        response[ACCESS_TOKEN_NAME_out] = f'Bearer {refresh.access_token}'

        return response

    def tokens_absent_or_invalid(self, request):
        """
        Doesn't add any headers.
        Used when both access and refresh headers expired."""
        return self.get_response(request)
