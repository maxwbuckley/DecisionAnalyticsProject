#! /usr/bin/python

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import numpy
import pandas
import lib.mcda_lib as mcda_lib

TOPLEVEL = set(["'Will they like it?'", "'Will they be good at it?'", 
                "'Can we afford them?'"])

WILLTHEYBEGOODAIT = set(["Soft Skills", "Technical Skills", "Experience",
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

QUESTIONS = [TOPLEVEL, WILLTHEYLIKEIT, WILLTHEYBEGOODAIT, CANWEAFFORDTHEM,
             TECHNICALSKILLS, EXPERIENCE, EDUCATION, ENOUGHRESPONSIBILITY]



def main():
  data = mcda_lib.getDataFromGoogleSpreadsheet()
  map_structure, keys = mcda_lib.getStructuredDataRollup(data)

  dataframe = mcda_lib.ConstructQuestionScoringMatrix(TOPLEVEL, map_structure)
  print dataframe


  norm_dataframe = mcda_lib.NormalizeDataFrame(dataframe)
  print norm_dataframe


  final_scores = mcda_lib.GetMarkovScoresList(norm_dataframe)
  print final_scores

if __name__ == "__main__":  
  main()
