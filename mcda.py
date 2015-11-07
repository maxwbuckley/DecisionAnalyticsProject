#! /usr/bin/python

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import numpy
import pandas
import lib.mcda_lib as mcda_lib

TOPLEVEL = set(["'Will they like it?'", "'Will they be good at it?'", 
                "'Can we afford them?'"])

WILLTHEYBEGOODATIT = set(["Soft Skills", "Technical Skills", "Experience",
                         "Education"])

TECHNICALSKILLS = set(["Programmming", "Databases", "Analytics/Statistics"])

EXPERIENCE = set(["Industry specificity", "Years of experience", 
                  "Job title relevance"])

EDUCATION = set(["School/College Name", "Strong Grades", "Course Relevance",
                 "Qualification Level (BSc/MSc/Phd)"])

WILLTHEYLIKEIT = set(["Cultural fit", "Career alignment/development",
                      "Personal development goals"])

CANWEAFFORDTHEM = set(["Monetary Price", "Enough Responsibility"])

ENOUGHRESPONSIBILITY = set([ "Seniority" ,"Reportees"])

QUESTIONS = [TOPLEVEL, WILLTHEYLIKEIT, WILLTHEYBEGOODATIT, CANWEAFFORDTHEM,
             TECHNICALSKILLS, EXPERIENCE, EDUCATION, ENOUGHRESPONSIBILITY]



def main():
  data = mcda_lib.getDataFromGoogleSpreadsheet()
  structured_data_dict, keys = mcda_lib.getStructuredDataRollup(data)

  mcda_lib.CalculateScores(WILLTHEYBEGOODATIT, structured_data_dict, False)
  mcda_lib.CalculateScores(EDUCATION, structured_data_dict, False)

if __name__ == "__main__":  
  main()
