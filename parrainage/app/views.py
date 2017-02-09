import logging

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView

from parrainage.app.models import Elu


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context


class EluListView(ListView):
    template_name = 'elu-list.html'

    def get_context_data(self, **kwargs):
        context = super(EluListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        qs = Elu.objects.all()
        if self.request.user.is_authenticated():
            if 'status' in self.request.GET:
                qs = qs.filter(status=self.request.GET['status'])
        if 'department' in self.request.GET:
            qs = qs.filter(department=self.request.GET['department'])
        if 'gender' in self.request.GET:
            qs = qs.filter(gender=self.request.GET['gender'])
        if 'nuance_politique' in self.request.GET:
            qs = qs.filter(
                nuance_politique=self.request.GET['nuance_politique'])
        if 'search' in self.request.GET:
            for word in self.request.GET['search'].split():
                qs = qs.filter(
                    Q(family_name__icontains=word) |
                    Q(city__icontains=word) |
                    Q(first_name__icontains=word)
                )
        if 'sort' in self.request.GET:
            sort = self.request.GET['sort']
            if sort == 'priority':
                qs = qs.order_by('priority', 'family_name', 'first_name')
            elif sort == 'status':
                qs = qs.order_by('status', 'family_name', 'first_name')
            else:
                qs = qs.order_by('family_name', 'first_name')
        else:
            qs = qs.order_by('family_name', 'first_name')
        return qs



class EluDetailView(DetailView):
    queryset = Elu.objects.all()
    template_name = 'elu-detail.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        self.object = self.get_object()
        action = request.POST.get('action')
        note = ''

        log = logging.getLogger()
        log.error('action = {}'.format(action))
        log.error('object = {}'.format(self.object))
        if action == 'assign':
            if self.object.assigned_to != request.user:
                note = 'Nouvelle assignation: {} → {}'.format(
                    self.object.assigned_to or '',
                    request.user)
                self.object.assigned_to = request.user
        elif action == 'unassign':
            if self.object.assigned_to == request.user:
                note = 'Nouvelle assignation: {} → {}'.format(
                    self.object.assigned_to or '', 'personne')
                self.object.assigned_to = None
        elif action == 'add_note':
            new_status = request.POST.get('status')
            if new_status:
                old_status = self.object.get_status_display()
                self.object.status = int(new_status)
                note = 'Nouveau statut: {} → {}\n'.format(
                    old_status, self.object.get_status_display())
            note += request.POST.get('note', '')
        elif action == 'update_contact':
            old_phone = self.object.private_phone
            old_email = self.object.private_email
            new_phone = request.POST.get('private_phone')
            new_email = request.POST.get('private_email')
            if old_phone != new_phone:
                note += 'Nouveau téléphone privé: {} → {}\n'.format(
                    old_phone, new_phone)
                self.object.private_phone = new_phone
            if old_email != new_email:
                note += 'Nouvel email privé: {} → {}'.format(
                    old_email, new_email)
                self.object.private_email = new_email

        if note:
            self.object.save()
            self.object.notes.create(user=request.user, note=note)
        return HttpResponseRedirect(self.object.get_absolute_url())

