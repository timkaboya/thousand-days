# encoding: utf-8

from django.db import models
from abc import ABCMeta, abstractmethod

class StoredErrorMessage(models.Model):
  text  = models.TextField()

  @staticmethod
  def fetch(cod):
    msg = StoredErrorMessage.objects.filter(code = cod)
    if msg:
      return msg[0].text
    else:
      news  = StoredErrorMessage(text = 'Error ' + cod, code = cod)
      news.save()
      return StoredErrorMessage.fetch(code)

class StoredSMS(models.Model):
  message = models.TextField()
  sender  = models.TextField()
  when    = models.DateTimeField(auto_now_add = True)

class SMSError(models.Model):
  pass
  # TODO: link this to StoredSMS.
