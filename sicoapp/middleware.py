from django.utils.deprecation import MiddlewareMixin

class COOPMiddleware(MiddlewareMixin):
    def process_response(self, request, response):

        # Establecer el encabezado para permitir el mismo origen
        response['Cross-Origin-Opener-Policy'] = 'same-origin'
        return response
