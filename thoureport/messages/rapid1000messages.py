# encoding: utf-8

from abc import ABCMeta, abstractmethod
import re
from thoureport.messages.parser import *

def and_join(dem, what):
  if len(dem) < 2: dem[0]
  return ', and '.join([', '.join(dem[0:-1]), dem[-1]])

class IDField(ThouField):
  @classmethod
  def is_legal(self, ans):
    return [] if len(ans) == 16 else 'pre_2'

class DateField(ThouField):
  @classmethod
  def is_legal(self, fld):
    ans = re.match(r'(\d{2})\.(\d{2})\.(\d{4})')
    if not ans: return 'pre_4'
    gps = ans.groups()
    return [] # Check that it is a valid date. TODO. Move to semantics part?

class NumberField(ThouField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'\d+', fld) else 'bad_number'

class CodeField(ThouField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'\w+', fld) else 'what_code'

class GravidityField(NumberField):
  pass

class ParityField(NumberField):
  pass

class PregCodeField(CodeField):
  @classmethod
  def expectations(self):
    return ['GS', 'MU', 'HD', 'RM', 'OL', 'YG', 'NR', 'TO', 'HW', 'NT', 'NT', 'NH', 'KX', 'YJ', 'LZ']

class PrevPregField(PregCodeField):
  @classmethod
  def expectations(self):
    return ['GS', 'MU', 'HD', 'RM']

class SymptomCodeField(CodeField):
  @classmethod
  def expectations(self):
    return ['AF', 'CH', 'CI', 'CM', 'IB', 'DB', 'DI', 'DS', 'FE', 'FP', 'HY', 'JA', 'MA', 'NP', 'NS',
            'OE', 'PC', 'RB', 'SA', 'SB', 'VO']

class RedSymptomCodeField(SymptomCodeField):
  @classmethod
  def invalid_error(self):
    return 'Please check that you have the correct type of current symptom or symptoms in the appropriate place in your Red Alert Report. These can be %s. If you have more than 1 they must be separated by a space.' % (and_join(self.expectations(), ', '))

  @classmethod
  def expectations(self):
    return ['AP', 'CO', 'HE', 'LA', 'MC', 'PA', 'PS', 'SC', 'SL', 'UN']

class LocationField(CodeField):
  @classmethod
  def expectations(self):
    return ['CL', 'HO', 'HP', 'OR']

class FloatedField(CodeField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'\w+\d+(\.\d+)?', fld) else 'bad_floated_field'

class NumberedField(CodeField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'\w+\d+', fld) else 'bad_numbered_field'

class HeightField(NumberedField):
  pass

class WeightField(FloatedField):
  pass

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
    return [] if re.match(r'0\d{15}', fld) else 'bad_phone_id'

class ANCField(NumberedField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'\w+\d', fld) else 'anc_code'

class PNCField(NumberedField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'\w+\d', fld) else 'pnc_code'

class NBCField(NumberedField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'\w+\d', fld) else 'nbc_code'

  @classmethod
  def expectations(self):
    return ['EBF', 'NB', 'PH', 'NBC1', 'NBC2', 'NBC3', 'NBC4', 'NBC5']

class GenderField(CodeField):
  @classmethod
  def expectations(self):
    return ['BO', 'GI']

class BreastFeedField(NBCField):
  @classmethod
  def expectations(self):
    return ['EBF', 'NB']

class InterventionField(CodeField):
  @classmethod
  def expectations(self):
    return ['PR', 'AA', 'AL', 'AT', 'NA']

class NBCInterventionField(InterventionField):
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

class VaccinationField(NumberedField):
  @classmethod
  def expectations(self):
    return ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'VC', 'VI', 'NV']

class VaccinationCompletionField(VaccinationField):
  @classmethod
  def expectations(self):
    return ['VC', 'VI', 'NV']

class MUACField(FloatedField):
  @classmethod
  def is_legal(self, fld):
    return [] if re.match(r'MUAC\d+(\.\d+)', fld) else 'bad_muac_code'

class DeathField(CodeField):
  @classmethod
  def expectations(self):
    return ['ND', 'CD', 'MD']

class ThouMsgError:
  def __init__(self, errors):
    self.errors     = errors

class ThouMessage:
  fields  = []

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
      return fh(nch[pz.code.lower()](pz))
    erh = lambda x: x
    try:
      erh = kwargs['error_handler']
    except KeyError:
      pass
    return erh(pz)

  @staticmethod
  def parse(msg):
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
        if type(fld) == type((1, 2)):
          cur, err, etc  = fld[0].pull(fld[0], cod, etc, fld[1])
          errors.extend(err)
        else:
          cur, err, etc  = fld.pull(fld, cod, etc)
          errors.extend(err)
        # fobs.extend(cur)
        fobs.append(cur)
      except ThouFieldError, err:
        errors.append(err.complaint)
    if etc.strip():
      errors.append('Superfluous text: "%s"' % (etc.strip(),))
    return klass(cod, fobs, errors)

  def __init__(self, cod, fobs, errs):
    self.code   = cod
    self.errors = errs
    def assembler(hsh, dat):
      hsh[dat.__class__.__name__.lower()] = dat
      return hsh
    self.fields = reduce(assembler, fobs, {})

  def __enter__(self):
    self.errors = self.errors.extend(self.semantics_check())
    if self.errors:
      raise ThouMsgError(self.errors)
    return self

  def __exit__(self, tp, val, tb):
    if tp:
      pass  # TODO: Record the error.
    else:
      pass  # TODO: Record the success.

  @abstractmethod
  def semantics_check(self):
    return ['Ariko Didier! I told you ThouMessage#semantics_check is abstract.']  # Hey, why doesn’t 'abstract' scream out? TODO.

class UnknownMessage(ThouMessage):
  pass

class PregMessage(ThouMessage):
  fields  = [IDField, DateField, DateField, GravidityField, ParityField,
              (PregCodeField, True),
              (SymptomCodeField, True),
             LocationField, WeightField, ToiletField, HandwashField]

class RefMessage(ThouMessage):
  fields  = [PhoneBasedIDField]

class ANCMessage(ThouMessage):
  fields  = [IDField, DateField, ANCField,
             (SymptomCodeField, True),
             LocationField, WeightField]

class DepMessage(ThouMessage):
  fields  = [IDField, NumberField, DateField]

class RiskMessage(ThouMessage):
  fields  = [IDField,
             (SymptomCodeField, True),
             LocationField, WeightField]

class RedMessage(ThouMessage):
  fields  = [(RedSymptomCodeField, True), LocationField]

class BirMessage(ThouMessage):
  fields  = [IDField, NumberField, DateField, GenderField,
             (SymptomCodeField, True),
             LocationField, BreastFeedField, WeightField]

class ChildMessage(ThouMessage):
  fields  = [IDField, NumberField, DateField, VaccinationField, VaccinationCompletionField,
             (SymptomCodeField, True),
             LocationField, WeightField, MUACField]

class DeathMessage(ThouMessage):
  fields  = [IDField, NumberField, DateField, LocationField, DeathField]

class ResultMessage(ThouMessage):
  fields  = [IDField,
             (SymptomCodeField, True),
             LocationField, InterventionField, MotherHealthStatusField]

class RedResultMessage(ThouMessage):
  fields  = [IDField, DateField,
             (SymptomCodeField, True),
             LocationField, InterventionField, MotherHealthStatusField]

class NBCMessage(ThouMessage):
  fields  = [IDField, NumberField, NBCField, DateField,
             (SymptomCodeField, True),
             BreastFeedField, NBCInterventionField, NewbornHealthStatusField]

class PNCMessage(ThouMessage):
  fields  = [IDField, PNCField, DateField,
             (SymptomCodeField, True),
             InterventionField, MotherHealthStatusField]


MSG_ASSOC = {
  'PRE':  PregMessage,
  'REF':  RefMessage,
  'ANC':  ANCMessage,
  'DEP':  DepMessage,
  'RISK': RiskMessage,
  'RED':  RedMessage,
  'BIR':  BirMessage,
  'CHI':  ChildMessage,
  'DTH':  DeathMessage,
  'RES':  ResultMessage,
  'RAR':  RedResultMessage,
  'NBC':  NBCMessage,
  'PNC':  PNCMessage,
}
