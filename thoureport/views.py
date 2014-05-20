from django.contrib import messages as flashes
from django.shortcuts import render, redirect
from thoureport.messages.rapid1000messages import *
from thoureport.reports.rapid1000reports import *
from thoureport.models import *

def smser(req):
  msgs  = StoredSMS.objects.all()
  return render(req, 'smser.html', {'msgs': msgs})

def history(req):
  msgs  = StoredSMS.objects.all()
  return render(req, 'history.html', {'msgs': msgs})

def sender(req):
  message               = req.POST['msg']
  req.session['phone']  = req.POST['phone']
  req.session['msg']    = message
  sm                    = StoredSMS(message = message, sender = req.POST['phone'])
  sm.save()
  def unknown(uk):
    flashes.add_message(req, flashes.ERROR, 'Unknown code: ' + message)
    return redirect('/')

  def has_errors(msgobj):
    for er in msgobj.errors:
      flashes.add_message(req, flashes.ERROR, er)
    return redirect('/')

  def is_fine(rept):
    rept.save()
    return redirect('thoureport.views.smser', name='smser')

  return ThouMessage.parse_report(req.POST['msg'], is_fine,
    {
      'RED':RedReport
    },
    error_handler   = has_errors,
    unknown_handler = unknown
  )
