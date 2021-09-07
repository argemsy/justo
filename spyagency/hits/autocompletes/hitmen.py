from dal import autocomplete
from django.db.models import Q
from users.models import User


class HitmenAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        queryset = User.objects.exclude(pk=1)
        if not self.request.user.groups.filter(name__iexact="big_boss").exists():
            # solo muestro a los integrantes de mi equipo y me excluyo
            # para evitar seleccionarme a mi mismo
            my_team = "team-manager-{}".format(str(self.request.user.pk).zfill(3))
            queryset = queryset.filter(groups__name__iexact=my_team).exclude(pk=self.request.user.pk)
        if self.q:
            queryset = queryset.filter(Q(email__istartswith=self.q) | Q(username__istartswith=self.q))
        return queryset
