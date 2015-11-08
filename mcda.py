#! /usr/bin/python

import matplotlib.pyplot as plt
import networkx as nx
import lib.mcda_lib as mcda_lib

TOPLEVEL = set(["'Will they like it?'", "'Will they be good at it?'", 
                "'Can we afford them?'"])

WILLTHEYBEGOODATIT = set(["Soft Skills", "Technical Skills", "Experience",
                         "Education"])

TECHNICALSKILLS = set(["Programming", "Databases", "Analytics/Statistics"])

EXPERIENCE = set(["Industry specificity", "Years of experience", 
                  "Job title relevance"])

EDUCATION = set(["School/College Name", "Strong Grades", "Course Relevance",
                 "Qualification Level (BSc/MSc/Phd)"])

WILLTHEYLIKEIT = set(["Cultural fit", "Career alignment/development",
                      "Personal development goals"])

CANWEAFFORDTHEM = set(["Monetary Price", "Enough Responsibility"])

ENOUGHRESPONSIBILITY = set([ "Seniority" ,"Reportees"])

QUESTIONS_DICT = {'ROOT' : TOPLEVEL, '\'Will they like it?\'' : WILLTHEYLIKEIT,
                  "'Will they be good at it?'" : WILLTHEYBEGOODATIT,
                  "'Can we afford them?'": CANWEAFFORDTHEM, "Technical Skills" :
                  TECHNICALSKILLS, "Education": EDUCATION, "Experience": EXPERIENCE,
                  "Enough Responsibility" : ENOUGHRESPONSIBILITY}


def main():
  scoring_default = False
  data = mcda_lib.getDataFromGoogleSpreadsheet()
  structured_data_dict, keys = mcda_lib.getStructuredDataRollup(data, scoring_default)
  all_edges = mcda_lib.GenerateCompleteGraph(QUESTIONS_DICT,
                                             structured_data_dict, scoring_default)
  graph = nx.DiGraph()
  for edge in all_edges:
    graph.add_edge(edge.source, edge.target, weight=edge.relative_weight)

  pos=nx.graphviz_layout(graph, prog='dot')
  nx.draw_networkx(graph, pos=pos, ax=None, with_labels=True, font_size=7)
  labels = nx.get_edge_attributes(graph,'weight')
  nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_size=7)

  plt.draw()
  #plt.savefig("graph.png", dpi=1000)
  #plt.show()
  print '\n\n'
  weights = mcda_lib.getEndLevelWeights(graph)
  cumulative_sum = 0
  for label, weight in weights:
    print label, weight
    cumulative_sum += weight
  print cumulative_sum
  #print graph.neighbors('Cultural fit')

if __name__ == "__main__":  
  main()
