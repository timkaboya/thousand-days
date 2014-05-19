# encoding: utf-8

from thoureport.messages.parser import *
from thousand.settings import DATABASES

# TODO:
# Save the report.
# Load the report(s).
# Find a report.
class ThouReport:
  created   = False

  @classmethod
  def create_table(self, mobj):
    sql = self.__creation_sql(mobj)

  @classmethod
  def table_name(self):
    return str(self).replace('.', '_').lower() + 's'

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
          subans  = ('%s_%s %s DEFAULT %s' % (col, exp.lower(), fldc.dbtype(), fldc.default_dbvalue()))
          cols.append(subans)
      else:
        cols.append('%s %s DEFAULT %s' % (col, fldc.dbtype(), fldc.default_dbvalue()))
    return (self.table_name(), cols)

  def __init__(self, msg):
    self.message  = msg

  def save(self):
    fds   = self.message.fields
    cols  = fds.keys()
    qry   = 'INSERT INTO %s (%s) VALUES (%s)' % (self.table_name(), ', '.join([col for col in cols]), ', '.join([fds[col].__class__.dbvalue(fds[col]) for col in cols]))
    if not self.__class__.created:
      # TODO: Conditionally create the table.
      raise Exception, ('Not yet creating DBs: ' + str(self.__creation_sql(self.message)))
      self.__class__.created = True
      return self.save()
    # TODO: run the INSERT.
    raise Exception, ('Not yet running queries: ' + qry)

  @classmethod
  def load(self, msgtxt):
    with ThouMessage.parse(msgtxt) as msg:
      return self(msg)
