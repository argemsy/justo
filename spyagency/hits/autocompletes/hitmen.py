from dal import autocomplete
from django.db.models import Q

from users.models import User


class HitmenAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        queryset = User.objects.exclude(pk=1)

        if self.q:
            queryset = queryset.filter(
                Q(email__istartswith=self.q) | Q(username__istartswith=self.q)
            )
        return queryset
