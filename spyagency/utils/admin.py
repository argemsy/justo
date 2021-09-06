from django.contrib import admin, messages


class BaseAdmin(admin.ModelAdmin):
    date_hierarchy = "pub_date"
    readonly_fields = ("transaction_id",)
    actions = ["change_status"]

    def change_status(self, request, queryset):
        if hasattr(self.model, "is_active"):
            model = self.model._meta.verbose_name
            n = queryset.count()
            message = f"{n} {model} editadas."
            self.message_user(request, message, messages.SUCCESS)
            for item in queryset:
                if item.is_active:
                    item.is_active = False
                else:
                    item.is_active = True
                item.save()
        return queryset

    change_status.short_description = "Editar status"
