# encoding: utf-8
#!/usr/bin/env python
# vim: ai ts=2 sts=4 et sw=4

from abc import ABCMeta, abstractmethod
import re
from datetime import *
from thoureport.messages.parser import *
from thoureport.reports.reports import THE_DATABASE as db

def first_cap(s):
  '''Capitalises the first letter (without assaulting the others like Ruby's #capitalize does).'''
  if len(s) < 1: return s
  return s[0].upper() + s[1:]

class IDField(ThouField):
  'The commonly-used ID field.'
  @classmethod
  def is_legal(self, ans):
    'For now, checks are limited to length assurance.'
    return [] if len(ans) == 16 else 'id_length'

class DateField(ThouField):
  'The descriptor for valid message fields.'
  @classmethod
  def is_legal(self, fld):
    ans = re.match(r'(\d{2})\.(\d{2})\.(\d{4})', fld)
    if not ans: return 'date_format_error'
    gps = ans.groups()
    return [] # Check that it is a valid date. To be Done.  Move to semantics part?

class LMPDateField(DateField):
  pass

class ANCDateField(DateField):
  pass

class NumberField(ThouField):
  'The descriptor for number fields.'
  @classmethod
  def is_legal(self, fld):
    'Basically a regex.'
    return [] if re.match(r'\d+', fld) else 'bad_number'

class CodeField(ThouField):
  'This should match basically any simple code, plain and numbered.'
  @classmethod
  def is_legal(self, fld):
    'Basically a simple regex.'
    return [] if re.match(r'\w+', fld) else 'what_code'

class GravidityField(NumberField):
  'Gravity is a number.'
  pass

class ParityField(NumberField):
  'Parity is a number.'
  pass

class PrevPregCodeField(CodeField):
  'Field for Previous pregnancy codes.'
  @classmethod
  def expectations(self):
    'Codes associated with previous pregnancy.'
    return ['GS', 'MU', 'HD', 'RM', 'OL', 'YG', 'NR', 'TO', 'HW', 'NT', 'NT', 'NH', 'KX', 'YJ', 'LZ']

class SymptomCodeField(CodeField):
  'Field for codes associated with symptoms.'
  @classmethod
  def expectations(self):
    'These are the codes associated with symptoms.'
    return ['AF', 'CH', 'CI', 'CM', 'IB', 'DB', 'DI', 'DS', 'FE', 'FP', 'HY', 'JA', 'MA', 'NP', 'NS',
            'OE', 'PC', 'RB', 'SA', 'SB', 'VO']

class RedSymptomCodeField(SymptomCodeField):
  @classmethod
  def expectations(self):
    return ['AP', 'CO', 'HE', 'LA', 'MC', 'PA', 'PS', 'SC', 'SL', 'UN']

class RiskSymptomCodeField(SymptomCodeField):
  @classmethod
  def expectations(self):
    return ['VO', 'PC', 'OE', 'NS', 'MA', 'JA', 'FP', 'FE', 'DS', 'DI', 'SA', 'RB', 'HY', 'CH', 'AF']

class ANCSymptomCodeField(SymptomCodeField):
  @classmethod
  def expectations(self):
    return ['VO', 'PC', 'OE', 'NS', 'MA', 'JA', 'FP', 'FE', 'DS', 'DI', 'SA', 'RB','NP', 'HY', 'CH', 'AF']

class ChiSymptomCodeField(SymptomCodeField):
  @classmethod
  def expectations(self):
    return ['NP', 'IB', 'DB']

class BirSymptomCodeField(SymptomCodeField):
  @classmethod
  def expectations(self):
    return ['SB', 'RB', 'NP', 'AF', 'CI', 'CM', 'IB', 'DB', 'PM']

class PNCSymptomCodeField(ANCSymptomCodeField):
  pass

class NBCSymptomCodeField(BirSymptomCodeField):
  pass

class CCMSymptomCodeField(SymptomCodeField):
  @classmethod
  def expectations(self):
    return ['DI', 'MA', 'PC', 'OI', 'NP', 'IB', 'DB', 'NV']

class CMRSymptomCodeField(CCMSymptomCodeField):
  pass

class LocationField(CodeField):
  @classmethod
  def expectations(self):
    return ['CL', 'HO', 'HP', 'OR']

class FloatedField(CodeField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'\w+\d+(.\d+)?$', fld) else 'bad_floated_field'

class NumberedField(CodeField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'\w+\d+$', fld) else 'bad_numbered_field'

class HeightField(FloatedField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'ht\d+(.\d+)?$', fld, re.IGNORECASE) else 'bad_height_code'

class WeightField(FloatedField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'wt\d+(.\d+)?$', fld, re.IGNORECASE) else 'bad_weight_code'

class ToiletField(CodeField):
  @classmethod
  def expectations(self):
    return ['TO', 'NT']

class HandwashField(CodeField):
  @classmethod
  def expectations(self):
    return ['HW', 'NH']

class PhoneBasedIDField(IDField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'\d{16}$', fld) else 'bad_phone_id'

class ANCField(NumberedField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'\w+\d$', fld) else 'anc_code'

  @classmethod
  def expectations(self):
    'Pre-enforcing the discipline that `is_legal` does not enforce.'
    return ['ANC2', 'ANC3', 'ANC4', 'ANC5']

class PNCField(NumberedField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'\w+\d$', fld) else 'pnc_code'

  @classmethod
  def expectations(self):
    'Pre-enforcing the discipline that `is_legal` does not enforce.'
    return ['PNC1', 'PNC2', 'PNC3', 'PNC4', 'PNC5']

class NBCField(NumberedField):
  'New-Born Care visit number is a ... number.'
  @classmethod
  def is_legal(self, fld):
    'Matches the code, not insisting on the string that precedes the number.'
    return [] if re.match(r'\w+\d$', fld) else 'nbc_code'

  @classmethod
  def expectations(self):
    'Pre-enforcing the discipline that `is_legal` does not enforce.'
    return ['NBC1', 'NBC2', 'NBC3', 'NBC4', 'NBC5']

class GenderField(CodeField):
  @classmethod
  def expectations(self):
    return ['BO', 'GI']

class BreastFeedField(CodeField):
  @classmethod
  def expectations(self):
    return ['BF1', 'NB']

class NBCBreastFeedField(BreastFeedField):
  @classmethod
  def expectations(self):
    return ['EBF', 'NB']

class CBNBreastFeedField(BreastFeedField):
  @classmethod
  def expectations(self):
    return ['EBF','CBF', 'NB']

class InterventionField(CodeField):
  @classmethod
  def expectations(self):
    return ['PR', 'AA', 'AL', 'AT', 'NA']

class RiskInterventionField(InterventionField):
  @classmethod
  def expectations(self):
    return ['PR', 'AA']

class RedInterventionField(InterventionField):
  @classmethod
  def expectations(self):
    return ['AL', 'AT', 'NA']

class NBCInterventionField(RiskInterventionField):
  pass

class PNCInterventionField(RiskInterventionField):
  pass

class CCMInterventionField(InterventionField):
  @classmethod
  def expectations(self):
    return ['PT', 'PR', 'TR', 'AA']

class CMRInterventionField(CCMInterventionField):
  pass

class HealthStatusField(CodeField):
  @classmethod
  def expectations(self):
    return ['MW', 'MS', 'CW', 'CS']

class NewbornHealthStatusField(HealthStatusField):
  @classmethod
  def expectations(self):
    return ['CW', 'CS']

class MotherHealthStatusField(HealthStatusField):
  @classmethod
  def expectations(self):
    return ['MW', 'MS']

class ChildStatusField(NewbornHealthStatusField):
  pass

class VaccinationField(NumberedField):
  'Vaccination Completion is apparently a number.'
  @classmethod
  def expectations(self):
    'The vaccination completion codes.'
    return ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'VC', 'VI', 'NV']

class VaccinationCompletionField(CodeField):
  @classmethod
  def expectations(self):
    return ['VC', 'VI', 'NV']

class MUACField(FloatedField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'MUAC|muac\d+(\.\d+)$', fld) else 'bad_muac_code'

class DeathField(CodeField):
  @classmethod
  def expectations(self):
    return ['ND', 'CD', 'MD']

class ThouMsgError:
  def __init__(self, errors):
    self.errors     = errors

class ThouMessage:
  '''Base class describing the standard RapidSMS 1000 Days message.'''
  fields  = []
  created = False

  # @staticmethod
  @classmethod
  def creation_sql(self, repc):
    cols  = [('created_at', 'TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()', 'No field class.', 'Created'),
             #  ('modified_at', 'TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()', 'No field class.', 'Modified')
             ]
    col   = None
    for fld in self.fields:
      if type(fld) == type((1, 2)):
        fldc  = fld[0]
        col   = str(fldc).split('.')[-1].lower()
        for exp in fldc.expectations():
          subans  = ('%s_%s' % (col, exp.lower()), '%s DEFAULT %s' % (fldc.dbtype(), fldc.default_dbvalue()), fldc, exp)
          cols.append(subans)
      else:
        col = str(fld).split('.')[-1].lower()
        cols.append((col, '%s DEFAULT %s' % (fld.dbtype(), fld.default_dbvalue()), fld, first_cap(fld.display())))
    return (str(repc).split('.')[-1].lower() + 's', cols)

  @classmethod
  def create_in_db(self, repc):
    try:
      tbl, cols = stuff = self.creation_sql(repc)
      if self.created: return stuff
      curz  = db.cursor()
      curz.execute('SELECT TRUE FROM information_schema.tables WHERE table_name = %s', (tbl,))
      if not curz.fetchone():
        curz.execute('CREATE TABLE %s (indexcol SERIAL NOT NULL);' % (tbl,))
        curz.close()
        return self.create_in_db(repc)
      for col in cols:
        curz.execute('SELECT TRUE FROM information_schema.columns WHERE table_name = %s AND column_name = %s', (tbl, col[0]))
        if not curz.fetchone():
          curz.execute('ALTER TABLE %s ADD COLUMN %s %s;' % (tbl, col[0], col[1]))
      curz.close()
      db.commit()
      self.created  = True
      return stuff
    except Exception, e:
      raise Exception, ('Table creation: ' + str(e))

  @staticmethod
  def pull_code(msg):
    return ((re.split(r'\s+', msg, 1)) + [''])[0:2]

  @staticmethod
  def caseless_hash(hsh):
    ans = {}
    for k in hsh:
      ans[k.lower()] = hsh[k]
    return ans

  @staticmethod
  def parse_report(msg, fh, hsh, **kwargs):
    pz  = ThouMessage.parse(msg)
    nch = ThouMessage.caseless_hash(hsh)
    if pz.__class__ == UnknownMessage:
      ukh = lambda x: x
      try:
        ukh = kwargs['unknown_handler']
      except KeyError:
        pass
      return ukh(pz)
    if not pz.errors:
      return fh(pz, nch[pz.code.lower()](pz))
    erh = lambda x: x
    try:
      erh = kwargs['error_handler']
    except KeyError:
      pass
    return erh(pz)

  @staticmethod
  def parse(msg):
    """ Called only once """ 
    #Pulls code from message to leave remaining string
    code, rem = ThouMessage.pull_code(msg.strip())
    klass     = UnknownMessage
    try:
      klass     = MSG_ASSOC[code.upper()]
    except KeyError:
      pass
    return klass.process(klass, code, rem)

  # “Private”
  @staticmethod
  def process(klass, cod, msg):
    errors  = []
    fobs    = []
    etc     = msg

    for fld in klass.fields:
      try:
        # Handle tuples (symptom code fields in this case)
        if type(fld) == type((1, 2)):
          cur, err, etc  = fld[0].pull(fld[0], cod, etc, fld[1])
        else:
          cur, err, etc  = fld.pull(fld, cod, etc)
          errors.extend(klass.db_checks(klass, cod, cur))
        
        errors.extend([(e, fld) for e in err])
        fobs.append(cur)
        #print "etc: ", etc, "cur subname: ", cur.subname(), "err: ", err
      except Exception, err:
        errors.append((str(err), fld))
    if etc.strip():
      errors.append('Superfluous text: "%s"' % (etc.strip(),))
    return klass(cod, fobs, errors)
  
  @staticmethod
  def db_checks(klass, cod, fld):
    """ Db checks for report code field. Method returns empty string if code is validated or relevant error if otherwise. """
    errors = []
    try:
      if cod.upper() == "PRE":
        value = fld.working_value[0].encode()
        if fld.display() == "id":
          curz  = db.cursor()
          # Check if Id is duplicated
          curz.execute('SELECT CASE WHEN EXISTS (SELECT * FROM pregreports WHERE idfield = %s) \
              THEN CAST(1 AS BIT) ELSE CAST(0 as BIT) END;', [value])
          if int(curz.fetchone()[0]):
            errors.append("duplicate_id")
        elif fld.display() == "lmpdate": 
          if not (klass.is_past_date(value) and klass.is_date_before(value, 9*30)):
            errors.append("invalid_LMPDate")
        elif fld.display() == "ancdate": 
          if not klass.is_date_before(value, 0):
            errors.append("past_ancdate")
        elif fld.display() == "gravidity":
          if not 0 < int(value) < 30: errors.append("gravidity_limit")
        elif fld.display() == "parity":
          if not 1 < int(value) < 30: errors.append("parity_limit")
        elif fld.display() == "weight":
          if not 35 < float((re.findall('\d+.\d|\d+',value))[0]) < 150: errors.append("weight_limit") 
        elif fld.display() == "height":
          if not 50 < float((re.findall('\d+.\d|\d+',value))[0]) < 250: errors.append("height_limit")
        else:
          pass
    except Exception, errors:
      pass

    return errors

  @staticmethod
  def is_past_date(date_str):
    """ Returns True if date is before current date or else False"""
    return False if (datetime.strptime(date_str, "%d.%m.%Y") > datetime.now()) else True

  @staticmethod
  def is_date_before(date_str, date_cmp):
    """ Returns True if date is not earlier than today - givendate or else False"""
    return False if (datetime.strptime(date_str, "%d.%m.%Y") < (datetime.now() - timedelta(days=date_cmp))) else True


  def __init__(self, cod, fobs, errs):
    self.code     = cod
    self.errors   = errs
    def as_hash(p, n):
      p[n.__class__.subname()] = n
      return p
    self.entries  = reduce(as_hash, fobs, {})

  def __enter__(self):
    self.errors = self.errors.append(self.semantics_check())
    if self.errors:
      raise ThouMsgError(self.errors)
    return self

  def __exit__(self, tp, val, tb):
    if tp:
      pass  # TODO: Record the error.
    else:
      pass  # TODO: Record the success.
  
  def error_check(self, msg):
    
    return []
  #@abstractmethod
  def semantics_check(self):

    return ['Semantics Check Error!']  # Hey, why doesn’t 'abstract' scream out? TODO.

class UnknownMessage(ThouMessage):

  '''To the Unknown Message.
Since every message has to be successfully parsed as a Message object, this is the one in the event that none other matches.'''
  pass


class PregMessage(ThouMessage):
  fields  = [IDField, LMPDateField, ANCDateField, GravidityField, ParityField,
              (PrevPregCodeField, True),
              (SymptomCodeField, True),
             LocationField, WeightField, HeightField, ToiletField, HandwashField]

class RefMessage(ThouMessage):
  fields  = [PhoneBasedIDField]

class ANCMessage(ThouMessage):
  fields  = [IDField, ANCDateField, ANCField,
             (ANCSymptomCodeField, True),
             LocationField, WeightField]

class DepMessage(ThouMessage):
  fields  = [IDField, NumberField, DateField]

class RiskMessage(ThouMessage):
  fields  = [IDField,
             (RiskSymptomCodeField, True),
             LocationField, WeightField]

class RedMessage(ThouMessage):
  fields  = [(RedSymptomCodeField, True), LocationField]

class BirMessage(ThouMessage):
  fields  = [IDField, NumberField, DateField, GenderField,
             (BirSymptomCodeField, True),
             LocationField, BreastFeedField, WeightField]

class ChildHealthMessage(ThouMessage):
  fields  = [IDField, NumberField, DateField, VaccinationField, VaccinationCompletionField,
             (ChiSymptomCodeField, True),
             LocationField, WeightField, MUACField]

class DeathMessage(ThouMessage):
  fields  = [IDField, NumberField, DateField, LocationField, DeathField]

class ResultMessage(ThouMessage):
  fields  = [IDField,
             (RiskSymptomCodeField, True),
             LocationField, RiskInterventionField, MotherHealthStatusField]

class RedResultMessage(ThouMessage):
  fields  = [IDField, DateField,
             (RedSymptomCodeField, True),
             LocationField, RedInterventionField, MotherHealthStatusField]

class NBCMessage(ThouMessage):
  fields  = [IDField, NumberField, NBCField, DateField,
             (NBCSymptomCodeField, True),
             NBCBreastFeedField, NBCInterventionField, NewbornHealthStatusField]

class CBNMessage(ThouMessage):
  fields  = [IDField, NumberField, DateField,
             CBNBreastFeedField, HeightField, WeightField, MUACField]

class CCMMessage(ThouMessage):
  fields  = [IDField, NumberField, DateField,
             (CCMSymptomCodeField, True),
             CCMInterventionField, MUACField]

class CMRMessage(ThouMessage):
  fields  = [IDField, NumberField, DateField,
             (CMRSymptomCodeField, True),
             CMRInterventionField, ChildStatusField]

class PNCMessage(ThouMessage):
  fields  = [IDField, PNCField, DateField,
             (PNCSymptomCodeField, True),
             PNCInterventionField, MotherHealthStatusField]

# Testing field. Takes any of my names.
class TimField(ThouField):
  @classmethod 
  def expectations(self):
    return ['Timothy', 'Kaboya', 'Kalimba']

class RevField(ThouField):
  @classmethod
  def expectations(self):
    return ['Revence', 'Kato', 'Kalibwani']

# Testing message.
class TIMMessage(ThouMessage):
  fields  = [(TimField, True)]

class REVMessage(ThouMessage):
  fields = [(RevField, True)]

MSG_ASSOC = {
  'PRE':  PregMessage,
  'REF':  RefMessage,
  'ANC':  ANCMessage,
  'DEP':  DepMessage,
  'RISK': RiskMessage,
  'RED':  RedMessage,
  'BIR':  BirMessage,
  'CHI':  ChildHealthMessage,
  'DTH':  DeathMessage,
  'RES':  ResultMessage,
  'RAR':  RedResultMessage,
  'NBC':  NBCMessage,
  'CBN':  CBNMessage,
  'CCM':  CCMMessage,
  'CMR':  CMRMessage,
  'PNC':  PNCMessage,

  'REV': REVMessage,
  'TIM':  TIMMessage,
}
