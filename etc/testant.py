# vim: ai ts=2 sts=2 et sw=2
from thoureport.reports import *
from thoureport.models import *

msg = 'RED DI'
rep = ThouMessage.parse_report(msg,
                  {'RED':RedReport})
rep.save()
