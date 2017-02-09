from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Elu(models.Model):

    GENDER_CHOICES = (
        ('H', 'Homme'),
        ('F', 'Femme'),
        ('', 'Inconnu'),
    )

    STATUS_NOTHING = 1
    STATUS_CONTACTED = 2
    STATUS_TO_CONTACT = 3
    STATUS_REFUSED = 10
    STATUS_ACCEPTED = 20

    STATUS_CHOICES = (
        (STATUS_NOTHING, 'Rien n\'a été fait'),
        (STATUS_CONTACTED, 'Élu contacté'),
        (STATUS_TO_CONTACT, 'Élu doit être recontacté'),
        (STATUS_REFUSED, 'Parrainage refusé'),
        (STATUS_ACCEPTED, 'Parrainage accepté'),
    )

    ROLE_CHOICES = (
        ('M', 'Maire'),
        ('CD', 'Conseiller départemental'),
        ('CR', 'Conseiller régional'),
        ('D', 'Député'),
    )

    first_name = models.CharField(max_length=255, db_index=True)
    family_name = models.CharField(max_length=255, db_index=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    comment = models.TextField(blank=True)

    priority = models.IntegerField(default=500)

    public_email = models.CharField(max_length=255, blank=True)
    public_phone = models.CharField(max_length=255, blank=True)
    public_website = models.URLField(max_length=255, blank=True)

    private_email = models.CharField(max_length=255, blank=True)
    private_phone = models.CharField(max_length=255, blank=True)

    status = models.IntegerField(default=STATUS_NOTHING, choices=STATUS_CHOICES,
                                 db_index=True)

    department = models.CharField(max_length=3, blank=True, db_index=True)
    city = models.CharField(max_length=255, blank=True, db_index=True)
    city_size = models.IntegerField(blank=True, null=True)
    city_code = models.CharField(max_length=10, blank=True)

    nuance_politique = models.CharField(max_length=5, blank=True, db_index=True)

    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    blank=True, null=True)

    def __str__(self):
        name = '{} {}'.format(self.first_name, self.family_name)
        if self.role == 'M':
            name += ' (Maire de {})'.format(self.city)
        elif self.role == 'CD':
            name += ' (Conseiller départemental {})'.format(self.department)
        elif self.role == 'CR':
            name += ' (Conseiller régional)'
        elif self.role == 'D':
            name += ' (Député)'
        return name

class Note(models.Model):
    elu = models.ForeignKey(Elu, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField()
