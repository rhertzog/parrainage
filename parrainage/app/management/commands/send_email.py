# Copyright 2017 Raphaël Hertzog
#
# This file is subject to the license terms in the LICENSE file found in
# the top-level directory of this distribution.

import argparse
from datetime import datetime
import logging

from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage, get_connection
from django.template import Template, Context
from django.db.models import Max

from parrainage.app.models import User, Elu

class Command(BaseCommand):
    help = 'Send a custom email to users'

    def add_arguments(self, parser):
        parser.add_argument('template', help='Path of the email template',
                            type=argparse.FileType(mode='r', encoding='utf-8'))
        parser.add_argument('--subject', help='Subject of the mail',
                            required=True)
        parser.add_argument('--send', help='Really send the email',
                            action='store_true')
        parser.add_argument('--attach', help='Attach a file to the mail',
                            action='append')
        parser.add_argument('--to', help='Send to given username only',
                            action='append')

    def handle(self, *args, **kwargs):
        template = Template(kwargs['template'].read())
        if kwargs['send']:
            connection = get_connection()
        else:
            connection = get_connection(
                backend='django.core.mail.backends.console.EmailBackend')
        msg = EmailMessage(
            from_email='Raphaël Hertzog <raphael@ouaza.com>',
            reply_to=['parrainage@listes.charlotte-marchandise.fr'],
            subject=kwargs['subject'],
            connection=connection,
        )
        if kwargs['attach']:
            for f in kwargs['attach']:
                msg.attach_file(f)

        userlist = User.objects.exclude(email='')
        if kwargs['to']:
            userlist = userlist.filter(username__in=kwargs['to'])

        for user in userlist:
            elus_a_traiter = []
            if hasattr(user, 'settings') and user.settings.department:
                elus_a_traiter = Elu.objects.filter(
                    assigned_to__isnull=True,
                    department=user.settings.department
                ).order_by('priority')[:5]
            elus_assignes = Elu.objects.filter(
                assigned_to=user,
                status__lt=Elu.STATUS_REFUSED,
            ).annotate(
                Max('notes__timestamp')
            ).order_by('notes__timestamp__max')


            context = Context({
                'user': user,
                'elus_a_traiter': elus_a_traiter,
                'elus_assignes': elus_assignes,
            })
            msg.body = template.render(context)
            msg.to = [user.email]
            msg.send()
