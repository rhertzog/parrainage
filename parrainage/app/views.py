import csv
import logging

from django.core.urlresolvers import reverse
from django.db.models import Q, Count, Max
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, View

from parrainage.app.models import Elu, User


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['departements'] = Elu.objects.only('department').values_list(
            'department', flat=True).distinct().order_by('department')
        context['user_count'] = User.objects.count()
        context['elus_contacted'] = Elu.objects.filter(
            status__gt=Elu.STATUS_NOTHING).count()
        context['elus_accepted'] = Elu.objects.filter(
            status=Elu.STATUS_ACCEPTED).count()

        if not self.request.user.is_authenticated():
            return context

        qs = Elu.objects.filter(status__gt=Elu.STATUS_NOTHING)
        qs = qs.values_list('department', 'status')

        stats = {}
        for department, status in qs:
            dep_stats = stats.setdefault(department, {
                'department': department,
                'parrainages': 0,
                'contacts': 0
            })
            dep_stats['contacts'] += 1
            if status == Elu.STATUS_ACCEPTED:
                dep_stats['parrainages'] += 1
        result = list(stats.values())
        result.sort(key=lambda x: (x['parrainages'], x['contacts']),
                    reverse=True)
        context['classement_departments'] = result

        context['classement_users'] = User.objects.annotate(
            count_elus=Count('elu', distinct=True)).annotate(
            count_notes=Count('notes', distinct=True)).order_by(
            '-count_notes', '-count_elus')

        context['my_elus'] = self.request.user.elu_set.filter(
            status__lt=Elu.STATUS_REFUSED).annotate(
                last_updated=Max('notes__timestamp')).order_by(
                    'status', 'last_updated')

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


class EluCSVForMap(View):

    def get(self, request, *args, **kwargs):
        qs = Elu.objects.exclude(city_latitude='').exclude(city_longitude='')
        status = request.GET.get('status', '')
        if status == 'nothing-done':
            qs = qs.exclude(status__gte=Elu.STATUS_REFUSED).filter(
                Q(status=Elu.STATUS_NOTHING) & Q(assigned_to__isnull=True))
        elif status == 'done':
            qs = qs.filter(status__gte=Elu.STATUS_REFUSED)
        elif status == 'in-progress':
            qs = qs.exclude(status__gte=Elu.STATUS_REFUSED).exclude(
                Q(status=Elu.STATUS_NOTHING) & Q(assigned_to__isnull=True))
        department = request.GET.get('department')
        if department:
            deplist = department.split(",")
            qs = qs.filter(department__in=deplist)
        try:
            limit = request.GET.get('limit')
            if limit:
                qs = qs[:int(limit)]
        except:
            pass

        response = HttpResponse(content_type='text/plain', charset='utf-8')
        csvwriter = csv.writer(response)
        csvwriter.writerow([
            'latitude', 'longitude', 'name', 'phone', 'email',
            'status', 'url'
        ])
        for elu in qs:
            csvwriter.writerow([
                elu.city_latitude,
                elu.city_longitude,
                str(elu),
                elu.public_phone,
                elu.public_email,
                elu.get_public_status_display(),
                request.build_absolute_uri(elu.get_absolute_url())
            ])

        return response
