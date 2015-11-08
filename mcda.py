#! /usr/bin/python
"""Reads and preps data from spreadsheet. Generates scores and plots them.
""" 

import sys
import lib.mcda_lib as mcda_lib


TOPLEVEL = set(['Will they like it?', 'Will they be good at it?', 
                'Can we afford them?'])

WILLTHEYBEGOODATIT = set(['Soft Skills', 'Technical Skills', 'Experience',
                         'Education'])

TECHNICALSKILLS = set(['Programming', 'Databases', 'Analytics/Statistics'])

EXPERIENCE = set(['Industry specificity', 'Years of experience', 
                  'Job title relevance'])

EDUCATION = set(['School/College Name', 'Strong Grades', 'Course Relevance',
                 'Qualification Level (BSc/MSc/Phd)'])

WILLTHEYLIKEIT = set(['Cultural fit', 'Career alignment/development',
                      'Personal development goals'])

CANWEAFFORDTHEM = set(['Monetary Price', 'Enough Responsibility'])

ENOUGHRESPONSIBILITY = set([ 'Seniority' ,'Reportees'])

QUESTIONS_DICT = {'ROOT': TOPLEVEL,
                  'Will they like it?': WILLTHEYLIKEIT,
                  'Will they be good at it?': WILLTHEYBEGOODATIT,
                  'Can we afford them?': CANWEAFFORDTHEM, 
                  'Technical Skills': TECHNICALSKILLS,
                  'Education': EDUCATION,
                  'Experience': EXPERIENCE,
                  'Enough Responsibility': ENOUGHRESPONSIBILITY}


def main():
  scoring_default = False
  #TODO(Max): Add a bias term for the alternative scoring system.
  data = mcda_lib.GetDataFromGoogleSpreadsheet(
      '13KcEqiK6tq2Vv72jK4np0kIAq2COlRVy1vPe_5DDrCk')
  structured_data_dict = mcda_lib.GetStructuredDataRollup(data, scoring_default)
  graph = mcda_lib.GenerateNetworkGraph(
      QUESTIONS_DICT, structured_data_dict, scoring_default)

  print '\n',
  weights = mcda_lib.GetEndLevelWeights(graph)
  for label, weight in weights:
    print label, weight
  print '\n',
  if len(sys.argv)>1:
    if sys.argv[1] == 'plot':
      mcda_lib.PlotNetworkGraph(graph)


if __name__ == '__main__':  
  main()
