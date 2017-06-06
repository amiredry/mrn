from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import datetime
from snippets import CountryField
from django.db import transaction
import random
import re
import hashlib
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from google.appengine.api import mail
from django.core.mail import mail_admins


try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class RegistrationManager(models.Manager):

    def activate_user(self, activation_key):

        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = self.model.ACTIVATED
                profile.save()
                return user
        return False

    def create_inactive_user(self, form1, form2, send_email=True):

        new_user = User.objects.create_user(form1["username"], form1["email"], form1["password1"], first_name = form1["first_name"], last_name = form1["last_name"])
        new_user.is_active = False
        new_user.save()


        registration_profile = self.create_profile(new_user, form2)

        if send_email:
            registration_profile.send_activation_email()

        return new_user
    create_inactive_user = transaction.commit_on_success(create_inactive_user)

    def create_profile(self, user, form2):

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = user.username
        activation_key = hashlib.sha1(salt+username).hexdigest()
        phone = form2["phone"]
        company = form2["company"]
        job_title = form2["job_title"]
        country = form2["country"]
        zipcode = form2["zipcode"]

        return self.create(user=user, activation_key=activation_key, phone=phone, company=company, job_title=job_title, country=country, zipcode=zipcode)


class UserProfile(models.Model):

    ACTIVATED = u"ALREADY_ACTIVATED"

    user = models.OneToOneField(User, primary_key=True, editable=False)
    phone = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    job_title =  models.CharField(max_length=255)
    country = CountryField.CountryField(default='US')
    zipcode = models.CharField(max_length=10)
    activation_key = models.CharField(_('activation key'), max_length=40)

    objects = RegistrationManager()

    def __unicode__(self):
        return self.user.username

    def activation_key_expired(self):

        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
            (self.user.date_joined + expiration_date <= datetime_now())
    activation_key_expired.boolean = True

    def send_activation_email(self):

        ctx_dict = {'activation_key': self.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                   }
        subject = render_to_string('qb_registration/activation_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string('qb_registration/activation_email.txt',
                                   ctx_dict)
        #enable to use django mail api
        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
        #disable to use django mail api
        #mail.send_mail("qbeats Support <aedry@shadowquant.com>", self.user.email, subject, message)