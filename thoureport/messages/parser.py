# encoding: utf-8

from abc import ABCMeta, abstractmethod
import re
import psycopg2

class ThouFieldError:
  def __init__(self, cpt):
    self.complaint  = cpt

# TODO:
# DB type.
# DB default.
# The value.
# The value, DB-ready.
# Insist on all that is expected (e.g., location on RED).
class ThouField:
  __metaclass__   = ABCMeta

  # TODO: fetch and list all the indicator fields.
  @staticmethod
  def pull(self, cod, txt, many = False):
    got = []
    etc = txt
    err = []
    while True:
      if not etc: break
      stuff = re.split(r'\s+', etc, 1)
      if len(stuff) < 2:
        stuff.append('')
      p1, etc = stuff
      ans     = p1.strip()
      etc     = etc.strip()
      if self.expected(ans):
        errs  = self.is_legal(ans)
        if errs:
          if type(errs) == type([]):
            err.extend(errs)
          else:
            err.append(errs)
        else:
          got.append(ans)
      else:
        # raise ThouFieldError("Invalid code (expected %s; not %s)" % (', '.join(self.expectations() or ['nothing']), ans))
        # err.append("Invalid code (expected %s; not %s)" % (cod, ', '.join(self.expectations() or ['nothing']), ans))
        err.append(self.invalid_error() or "Invalid code (expected %s; not %s)" % (', '.join(self.expectations() or ['nothing']), ans))
      if not many: break
    return (self(got, many), err, etc)

  @classmethod
  @abstractmethod
  def is_legal(self, fld):
    pass

  @classmethod
  @abstractmethod
  def invalid_error(self):
    return 'Please check that you have the correct data. Expecting: %s.' % (', '.join(self.expectations()),)

  @classmethod
  @abstractmethod
  def expectations(self):
    return []

  @classmethod
  def expected(self, fld):
    for exp in self.expectations():
      if exp.lower() == fld.lower():
        return True
    return False

  @classmethod
  def fixed_for_db(self, val):
    if type(val) == type(None):
      return 'NULL'
    if type(val) in [type(x) for x in [1, 1.0]]:
      return str(val)
    if val in self.expectations():
      return self.fixed_for_db(self.expectations().index(val))
    if type(val) == type(''):
      return str("'%s'" % (val,)) # TODO: Proper SQL escapes, valid for current engine.

  @classmethod
  def dbtype(self, it = None):
    return 'TEXT'    # TODO.

  @classmethod
  def dbvalue(self, it):
    return 'self.fixed_for_db(it.working_value)'    # TODO.

  @classmethod
  def default_dbvalue(self):
    # return self.fixed_for_db(self.default_value)
    return self.fixed_for_db(None)

  def __init__(self, val, many):
    self.working_value  = val
    self.several_fields = many
