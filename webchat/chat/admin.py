
from django.contrib import admin
from .models import Thread, Message

'''Chat rooms in admin panel'''


class ThreadAdmin(admin.ModelAdmin):

    list_display = ('id', "creater", "created")

# Beautiful filter tab in admin panel
    filter_horizontal = ("participant", )


'''For messages in admin panel'''


class MessageAdmin(admin.ModelAdmin):

    list_display = ("thread", "sender", "text", "created")


admin.site.register(Message, MessageAdmin)
admin.site.register(Thread, ThreadAdmin)
