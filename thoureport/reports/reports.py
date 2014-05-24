# encoding: utf-8

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

  @classmethod
  def sql_description(self, mobj):
    return self.__creation_sql(mobj)

  @classmethod
  def table_name(self):
    return str(self).split('.')[-1].lower() + 's'

  @classmethod
  def __creation_sql(self, mobj):
    fields      = mobj.fields
    raise Exception, [x for x in fields]
    columns     = mobj.fields.keys()
    cols        = []
    for col in columns:
      fld   = fields[col]
      fldc  = fld.__class__
      if fld.several_fields:
        for exp in fld.expectations():
          subans  = (('%s_%s' % (col, exp.lower()), '%s DEFAULT %s' % (fldc.dbtype(), fldc.default_dbvalue()), fldc))
          cols.append(subans)
      else:
        cols.append((col, '%s DEFAULT %s' % (fldc.dbtype(), fldc.default_dbvalue()), fldc))
    return (self.table_name(), cols)

  def __init__(self, msg):
    self.message  = msg

  def __ensure_table(self):
    dbn, _ = self.__creation_sql(self.message)
    if not self.__class__.created:
      curz  = THE_DATABASE.cursor()
      curz.execute('SELECT TRUE FROM information_schema.tables WHERE table_name = (%s)', [dbn])
      row = curz.fetchone()
      if not row:
        curz.execute('CREATE TABLE %s ();' % (dbn,))
      curz.close()
      self.__class__.created = True
    return dbn

  def __ensure_columns(self):
    dbn, cols = self.__creation_sql(self.message)
    if not self.__class__.columned:
      curz  = THE_DATABASE.cursor()
      curz.execute('SELECT column_name FROM information_schema.columns WHERE table_name = (%s)', [dbn])
      noms  = set()
      while True:
        row = curz.fetchone()
        if not row: break
        noms.add(row[0])
      for coln, coletc, cc in cols:
        if not (coln in noms):
          curz.execute('ALTER TABLE %s ADD COLUMN %s %s; /*%s*/' % (dbn, coln, coletc, str(cc)))
      curz.close()
      self.__class__.columned = True
    return cols

  def __insertables(self):
    fds = self.message.fields
    cvs = {}
    for fx in fds:
      curfd = fds[fx]
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
    tbl   = self.__ensure_table()
    cols  = self.__ensure_columns()
    cvs   = self.__insertables()
    curz  = THE_DATABASE.cursor()
    cpt   = []
    vpt   = []
    for coln, _, escer in cols:
      if coln in cvs:
        cpt.append(coln)
        vpt.append(escer.dbvalue(cvs[coln], curz))
    qry   = 'INSERT INTO %s (%s) VALUES (%s);' % (tbl, ', '.join(cpt), ', '.join(vpt)) 
    curz.execute(qry)
    curz.close()
    return self

  @classmethod
  def load(self, msgtxt):
    with ThouMessage.parse(msgtxt) as msg:
      return self(msg)
