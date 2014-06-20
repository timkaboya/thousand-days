# encoding: utf-8
#!/usr/bin/env python
# vim: ai ts=2 sts=4 et sw=4


from thoureport.messages.parser import *
from thousand.settings import DATABASES
import psycopg2
import re

__DEFAULTS    = DATABASES['default']
THE_DATABASE  = psycopg2.connect(database = __DEFAULTS['NAME'],
                                     user = __DEFAULTS['USER'],
                                 password = __DEFAULTS['PASSWORD'],
                                     host = __DEFAULTS['HOST'])

# TODO:
# Load the report(s).
# Find a report.
class ThouReport:
  created   = False
  columned  = False

  def __init__(self, msg):
    self.msg  = msg

  def __insertables(self, fds):
    cvs   = {}
    ents  = self.msg.entries
    for fx in ents:
      curfd = ents[fx]
      if curfd.several_fields:
        for vl in curfd.working_value:
          cvs[('%s_%s' % (fx, vl)).lower()] = vl
      else:
        try:
          cvs[fx] = curfd.working_value[0]
        except IndexError:
          raise Exception, ('No value supplied for column \'%s\' (%s)' % (fx, str(curfd)))
    return cvs

  def save(self):
    tbl, cols = self.msg.__class__.create_in_db(self.__class__)
    cvs       = self.__insertables(cols)
    curz      = THE_DATABASE.cursor()
    cpt       = []
    vpt       = []
    for coln, _, escer, _ in cols:
      if coln in cvs:
        cpt.append(coln)
        vpt.append(escer.dbvalue(cvs[coln], curz))
    qry = 'INSERT INTO %s (%s) VALUES (%s) RETURNING indexcol;' % (tbl, ', '.join(cpt), ', '.join(vpt)) 
    curz.execute(qry)
    ans = curz.fetchone()[0]
    curz.close()
    return ans

  @classmethod
  def load(self, msgtxt):
    with ThouMessage.parse(msgtxt) as msg:
      return self(msg)
