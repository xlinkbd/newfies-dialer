#
# Newfies-Dialer License
# http://www.newfies-dialer.org
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2013 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from user_profile.models import Profile_abstract
from survey.models import Survey


class AR_Setting(models.Model):
    """This defines the Appointment Reminder settings to apply to a ar_user

    **Attributes**:

        * ``cid_number`` - CID number.
        * ``cid_name`` - CID name
        * ``call_timeout`` - call timeout
        * ``user`` - Newfies User
        * ``survey`` - Frozen Survey

    **Name of DB table**: appointment_reminder_setting
    """
    cid_number = models.CharField(max_length=50, blank=False, null=True,
                                  verbose_name=_("CID number"),
                                  help_text=_("CID number"))
    cid_name = models.CharField(max_length=50, blank=False, null=True,
                                verbose_name=_("CID name"),
                                help_text=_("CID name"))
    call_timeout = models.IntegerField(default='3', blank=True, null=True,
                                       verbose_name=_('call timeout'),
                                       help_text=_("call timeout"))
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=_("user"),
                             help_text=_("select user"),
                             related_name="appointment_reminder_user")
    survey = models.ForeignKey(Survey, null=True, blank=True,
                               verbose_name=_('frozen survey'),
                               related_name="appointment_reminder_survey")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '[%s] %s' % (self.id, self.name)

    class Meta:
        verbose_name = _("AR setting")
        verbose_name_plural = _("AR settings")
        db_table = "appointment_reminder_setting"


class AR_User(User):
    """appointment reminder User Model"""

    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = _('AR user')
        verbose_name_plural = _('AR users')

    def save(self, **kwargs):
        if not self.pk:
            self.is_staff = 0
            self.is_superuser = 0
        super(AR_User, self).save(**kwargs)

    def is_ar_user(self):
        try:
            AR_UserProfile.objects.get(user=self)
            return True
        except:
            return False
    User.add_to_class('is_ar_user', is_ar_user)


class AR_UserProfile(Profile_abstract):
    """This defines extra features for the AR_user

    **Attributes**:

        * ``ar_dialersetting`` - appointment reminder settings


    **Name of DB table**: ar_user_profile
    """
    ar_dialersetting = models.ForeignKey(AR_Setting, null=True, blank=True,
                                         verbose_name=_('appointment reminder settings'))

    class Meta:
        db_table = 'ar_user_profile'
        verbose_name = _("AR user profile")
        verbose_name_plural = _("AR user profiles")

    def __unicode__(self):
        return u"%s" % str(self.user)