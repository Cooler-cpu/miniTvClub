from django.contrib import admin

from .models import TokenType, Token


admin.site.register(TokenType)
admin.site.register(Token)