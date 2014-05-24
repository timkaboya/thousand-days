from django.contrib import messages as flashes
from django.shortcuts import render, redirect
from thoureport.messages.rapid1000messages import *
from thoureport.reports.rapid1000reports import *
from thoureport.reports.reports import THE_DATABASE as db
from thoureport.models import *

REPORT_SET = {
  'RED':  RedReport,
}

class TraversibleReport:
  def __init__(self, repc):
    self.repc = repc

  def columns(self):
    raise Exception, self.repc.create_table()

def smser(req):
  msgs  = StoredSMS.objects.all()
  return render(req, 'smser.html', {'msgs': msgs})

def reports(req, rcode = None):
  reps  = []
  if rcode:
    try:
      reps  = [(REPORT_SET[rcode[1:]], MSG_ASSOC[rcode[1:]])]
    except Exception, e:
      pass
  raise Exception, reps[0][1].fields
  raise Exception, reps[0][0].sql_description(reps[0][1])
  return render(req, 'reports.html', {'reps': reps, 'repset': REPORT_SET})

def messages(req):
  msgs  = StoredSMS.objects.all()
  return render(req, 'messages.html', {'msgs': msgs})

def resp_mod(req, cod):
  try:
    msg       = StoredResponse.objects.get(code = cod)
    msg.text  = req.POST['msg']
    msg.save()
  except Exception, e:
    StoredResponse.objects.create(code = req.POST['code'], text = req.POST['msg'])
  return redirect('/responses')

def responses(req):
  msgs  = StoredResponse.objects.all()
  return render(req, 'responses.html', {'msgs': msgs})

def sender(req):
  message               = req.POST['msg']
  req.session['phone']  = req.POST['phone']
  req.session['msg']    = message
  sm                    = StoredSMS(message = message, sender = req.POST['phone'])
  sm.save()
  def unknown(uk):
    flashes.add_message(req, flashes.ERROR, StoredResponse.fetch('unknown_message'))
    return redirect('/')

  def has_errors(msgobj):
    for er in msgobj.errors:
      flashes.add_message(req,
        flashes.ERROR,
        StoredResponse.fetch(er)
      )
    return redirect('/')

  def is_fine(rept):
    rept.save()
    return redirect('/')

  return ThouMessage.parse_report(req.POST['msg'], is_fine, REPORT_SET, error_handler   = has_errors, unknown_handler = unknown)
