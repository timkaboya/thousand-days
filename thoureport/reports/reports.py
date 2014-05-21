# encoding: utf-8

from thoureport.messages.parser import *
from thousand.settings import DATABASES
import psycopg2
import re
import sets

__DEFAULTS    = DATABASES['default']
THE_DATABASE  = psycopg2.connect(database = __DEFAULTS['NAME'],
                                     user = __DEFAULTS['USER'],
                                 password = __DEFAULTS['PASSWORD'],
                                     host = __DEFAULTS['HOST'])

# TODO:
# IDs for records.
# Save the report.
# Load the report(s).
# Find a report.
class ThouReport:
  created   = False
  columned  = False

  @classmethod
  def create_table(self, mobj):
    sql = self.__creation_sql(mobj)

  @classmethod
  def table_name(self):
    return str(self).split('.')[-1].lower() + 's'

  @classmethod
  def __creation_sql(self, mobj):
    fields      = mobj.fields
    columns     = mobj.fields.keys()
    cols        = []
    for col in columns:
      fld   = fields[col]
      fldc  = fld.__class__
      if fld.several_fields:
        for exp in fld.expectations():
          subans  = (('%s_%s' % (col, exp.lower()), '%s DEFAULT %s' % (fldc.dbtype(), fldc.default_dbvalue())))
          cols.append(subans)
      else:
        cols.append((col, '%s DEFAULT %s' % (fldc.dbtype(), fldc.default_dbvalue())))
    return (self.table_name(), cols)

  def __init__(self, msg):
    self.message  = msg

  def __ensure_table(self):
    if not self.__class__.created:
      dbn, _ = self.__creation_sql(self.message)
      curz  = THE_DATABASE.cursor()
      curz.execute('SELECT TRUE FROM information_schema.tables WHERE table_name = (%s)', [dbn])
      row = curz.fetchone()
      if not row:
        curz.execute('CREATE TABLE %s ();' % (dbn,))
      curz.close()
      self.__class__.created = True

  def __ensure_columns(self):
    if not self.__class__.columned:
      dbn, cols = self.__creation_sql(self.message)
      curz  = THE_DATABASE.cursor()
      curz.execute('SELECT column_name FROM information_schema.columns WHERE table_name = (%s)', [dbn])
      noms  = sets.Set()
      while True:
        row = curz.fetchone()
        if not row: break
        noms.add(row[0])
      for coln, coletc in cols:
        # n, _  = re.split(r'\s+', col, 1)
        if not (coln in noms):
          curz.execute('ALTER TABLE %s ADD COLUMN %s %s;' % (dbn, coln, coletc))
      curz.close()
      self.__class__.columned = True

  def save(self):
    if not self.__class__.created:
      self.__ensure_table()
    if not self.__class__.columned:
      self.__ensure_columns()
    fds       = self.message.fields
    given     = sets.Set([('%s_%s' % (x, fds[x].working_value)) for x in fds if fds[x].several_fields])
    tbl, cols = self.__creation_sql(self.message)
    cpt       = []
    vpt       = []
    # TODO: given should be filled properly. Need to sleep.
    raise Exception, given
    for coln, _ in cols:
      if coln in given:
        cpt.append(coln)
        vpt.append("'%s'" % (str(coln),))   # TODO: Mogrify properly.
      # vpt.append(fds[coln].__class__.dbvalue(fds[coln]))  # TODO. To-do the below.
    qry   = 'INSERT INTO %s (%s) VALUES (%s);' % (tbl, ', '.join(cpt), ', '.join(vpt)) 
    raise Exception, qry
    raise Exception, fds
    curz  = THE_DATABASE.cursor()
    curz.execute(qry)
    curz.close()
    return self

  @classmethod
  def load(self, msgtxt):
    with ThouMessage.parse(msgtxt) as msg:
      return self(msg)
