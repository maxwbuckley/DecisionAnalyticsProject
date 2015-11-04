#! /usr/bin/python

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

TOPLEVEL = set(["'Will they like it?'", "'Will they be good at it?'", "'Can we afford them?'"])

WILLTHEYBEGOODAIT = set(["Soft Skills", "Technical Skills", "Experience", "Education"])

TECHNICALSKILLS = set(["Programmming", "Databases", "Analytics/Statistics"])

EXPERIENCE = set(["Industry specificity", "Years of experience", "Job title relevance"])

EDUCATION = set(["School/College Name", "Strong Grades", "Course Relevance",
                 "Qualification Level (BSc/MSc/Phd)"])

WILLTHEYLIKEIT = set(["Cultural fit", "Career alignment/development",
                      "Personal development goals"])

CANWEAFFORDTHEM = set(["Monetary Price", "Enough Responsibility"])

ENOUGHRESPONSIBILITY = set([ "Seniority" ,"Reportees"])

QUESTIONS = [TOPLEVEL, WILLTHEYLIKEIT, WILLTHEYBEGOODAIT, CANWEAFFORDTHEM,
             TECHNICALSKILLS, EXPERIENCE, EDUCATION, ENOUGHRESPONSIBILITY]

def getDataFromGoogleSpreadsheet():
  json_key = json.load(open('MCDA-UCD-8b0b964e491d.json'))
  scope = ['https://spreadsheets.google.com/feeds']

  credentials = SignedJwtAssertionCredentials(
      json_key['client_email'], json_key['private_key'].encode(), scope)

  gc = gspread.authorize(credentials)
  wks = gc.open_by_key(
      "13KcEqiK6tq2Vv72jK4np0kIAq2COlRVy1vPe_5DDrCk").get_worksheet(0)

  cell_list = wks.get_all_records()

  return cell_list

def getRelevantSet(value):
  for question_set in QUESTIONS:
    if value in question_set:
      return question_set

def getDataStructureRollup(data):
  map_values = {}
  keys = [key for key in data[0].keys()]
  split_keys = set()
  for key in keys:
    map_values[key] = set(key.split(' or '))
    split_keys = split_keys.union(set(key.split(' or ')))

  return map_values, split_keys

data = getDataFromGoogleSpreadsheet()
structure, keys = getDataStructureRollup(data)


print keys
