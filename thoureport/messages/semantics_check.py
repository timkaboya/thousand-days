# encoding: utf-8
#!/usr/bin/env python
# vim: ai ts=2 sts=4 et sw=4

#from abc import ABCMeta, abstractmethod
#import re
#from thoureport.messages.parser import *
#from thoureport.reports.reports import THE_DATABASE as db


def semantics_check(self):
  ####
  #### Pregnancy Semantic and DB Checks
  # Patient ID checks (IDField)
  # If National_id: refuse if id is duplicate (Already Used), 
  # If phonenumber+date, verify chw phone number, compare date with range (curr_date-5)
  ## Last Menstrual Period
  # Should be less than curr_date and not earlier than Curr_date-9months
  ## Second ANC Date
  # Greater than curr_date but not later than calculated exp_delivery_date
  ## Gravidity
  # Should Be btn 01 and 30, (should we store it as num)
  # Should not be less than registered Pregnancies for given ID
  ## Parity
  # Should be less than Gravidity. 
  ## Previous Symptoms
  # If Gravidity is 1, Previous should be "NR"
  # RM only reported if (gravidity-parity >= 2)
  # Check for code duplication
  # if NR is reported, no other code should be reported. 
  ## Current Symptoms
  # if NP reported, no other code should be reported
  ## Location (No semantic Check)
  ## Mother Weight: Should be btn 35 and 150
  ## Mother height: Should be btn 50 n 250 
  ## Toilet (No Semantic Check)
  ## HandWashing (No Semantic Check)
    
  ### Other Constraints
  # Refuse PRE Report 
  #if  BIR is reported recently, miscarriage, death reported,
  # (previous LMP - new LMP > 10 months)
  #   
  
  return ['No Kalibwani, Stop it.! I told you ThouMessage#semantics_check is abstract.']  # Hey, why doesn’t 'abstract' scream out? TOdo.

def ANC_Check(self):
  ### Pre must already be recorded 
  ## NumberField: Same checks as PRE
  ## ANC Visit Date
  # <= CurrentDate, <= (LMP + 9 Months)
  # Date should be > Previous ANC
  ## ANC Visit Number
  # ANC Visits can't be duplicated and should be in sequence
  ## Curr Symptoms
  # If NP reported, No other code.
  ## Location
  ## Mother Weight: btn 35 and 150

def RISK_Check(self):
  ### PRE must be already recorded
  ## NumberField: Same checks
  ## Curr Symptoms: Can't report "NP"
  ## Location: 
  ## Weight: Weight btn 25 and 150. 

def RES_Check(self):
  ### PRE must be already recorded
  ## NumberField: Same checks
  ## Reported Symptoms: Should be same as RISK
  ## Location:
  ## Intervention Code:
  ## Mother Status: 

def RED_Check(self):
  ## None... 

def RAR_Check(self):
  ## NumberField, same check
  ## Emergency Date: <= Curr_date, Match with Red Alert??
  ## Reported Symptoms: Compare with RED, How?
  ## Location: 
  ## Intervention Code: Mother Status

def BIR_Check(self):
  ## Can be duplicated with Diff Child Number
  ## NumberField, check
  ## Child Number: Btn 01 and 08. No duplicate child number
  ## Date of Delivery <= Curr_date
  # If Woman is registered as PRE, then LMP + DOD < 9 months
  ## Gender, Curr Symptoms (If NP reported, no other code), Location, BF, 
  ## Child Weight (Btn 1 and 10)

def NBC_Check(self):
  ## Only when BIR is reported
  # No duplicate NBC visit for same child number
  ## NumberField, check
  ## ChildNumber (01, 08), 
  ##NBC Number: Curr_Date must be < DOB+60days, NBC2 must preceed NBC1...
  ## DOB: <= curr_date, DOB must be equal to saved BIR_DOB
  ## Curr Symptoms: If NP is reported, no other. 
  ## Breastfeeding: InterventionCode, Child_Status, 

def main():
  print "Hello World"

if __name__ == "__main__":
  main()
