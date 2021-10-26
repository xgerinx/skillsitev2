from django.contrib import admin

from .models import (Post, Order, Review, Leader, Main_review, HomeData, Client, Switch)


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title", "content"]

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Leader)
admin.site.register(Main_review)
admin.site.register(HomeData)
admin.site.register(Client)
admin.site.register(Switch)