from django.contrib import admin
from .models import (
    Role,
    User,
    Post,
    Image,
    ImageComment,
    PostComment
)

# Register your models here.

admin.register(Role)(admin.ModelAdmin)
admin.register(User)(admin.ModelAdmin)
admin.register(Post)(admin.ModelAdmin)
admin.register(PostComment)(admin.ModelAdmin)
admin.register(Image)(admin.ModelAdmin)
admin.register(ImageComment)(admin.ModelAdmin)
