# encoding: utf-8
# vim: ai ts=2 sts=2 et sw=2

from django.contrib import admin
from django.db import models
from abc import ABCMeta, abstractmethod

class StoredResponse(models.Model):
  text  = models.TextField()
  code  = models.TextField()

  @staticmethod
  def fetch_tranform(cod, msg):
    ans = StoredResponse.fetch(cod)
    # TODO: Apply transformations, from the same descriptor that shows them to the admin.
    return ans

  @staticmethod
  def fetch(cod):
    msg = StoredResponse.objects.filter(code = cod)
    if msg.count():
      return msg[0].text
    else:
      news  = StoredResponse(text = 'Error code: ' + cod, code = cod)
      news.save()
      return StoredResponse.fetch(cod)

class StoredSMS(models.Model):
  message = models.TextField()
  sender  = models.TextField()
  when    = models.DateTimeField(auto_now_add = True)

class SMSError(models.Model):
  pass
  # TODO: link this to StoredSMS.
