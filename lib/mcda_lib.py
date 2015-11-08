
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import numpy
import pandas
from collections import namedtuple
import networkx

Edge = namedtuple('Edge', ['source', 'target', 'relative_weight'])

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


def getStructuredDataRollup(data, scoring_default=True):
  return_list = []
  split_keys = set()
  for data_dict in data:
    map_values = {}
    for key, value in data_dict.iteritems():
      if key != "Timestamp":
        keyword1, keyword2 = key.split(' or ')
        # This is where I assign the scores that ends up in the final matrices.
        map_values[key] = scoringDictionary(keyword1, keyword2, value, scoring_default)
        split_keys = split_keys.union(set([keyword1, keyword2]))
    return_list.append(map_values)
  return return_list, split_keys

def scoringDictionary(keyword1, keyword2, value, default=True):
  if default:
    return  {keyword1: 8-value, keyword2: value}
  else:
    return  {keyword1: max(4-value,0), keyword2: max(value-4,0)}
    


def ConstructQuestionScoringMatrix(question_set, structured_data_dict,
                                   scoring_default=True):
  n = len(question_set)
  question_list = sorted([question for question in question_set])
  if scoring_default:
    zero_mat = numpy.zeros((n,n))
  else:
    zero_mat = (numpy.ones((n,n))-numpy.identity(n))*.1
  df = pandas.DataFrame(zero_mat, index=question_list, columns=question_list)
  for row in structured_data_dict:
    for key, value in row.iteritems():
      # key is the question and value is a dict of keyword to score.
      keyword1, keyword2 = key.split(' or ')
      # Just need to check the first of the or words
      if keyword1 in question_set:
        df[keyword1][keyword2] += value[keyword2]
        df[keyword2][keyword1] += value[keyword1]
  return df


def NormalizeDataFrame(data_frame):
  new_df = data_frame /data_frame.sum()
  return new_df



def GetMarkovScoresList(QuestionSquareMatrix):
  n = len(QuestionSquareMatrix)
  if n==2:
    labels = list(QuestionSquareMatrix.index)
    tempframe = QuestionSquareMatrix/QuestionSquareMatrix.sum().sum()
    scores = ( tempframe[labels[1]][0], tempframe[labels[0]][1])
    return zip(labels, scores)
  NormalizedSquareMatrix = NormalizeDataFrame(QuestionSquareMatrix)
  transition_matrix = numpy.linalg.matrix_power(NormalizedSquareMatrix, 1000)
  # Need an n * 1 matrix of 1/n to multiply by the transition matrix
  fractional_score_matrix = numpy.ones((n,1))*(1/(n*1.0))
  final_score = numpy.dot(transition_matrix, fractional_score_matrix)
  labels = list(NormalizedSquareMatrix.index)
  output = zip(labels, final_score)
  return output


def GenerateGraphEdges(source_node, markov_score_list):
  edge_list = []
  for score in markov_score_list:
    edge_list.append(Edge(source_node, score[0], score[1]))
  return edge_list


def GenerateCompleteGraph(question_dict, structured_data_dict, scoring_default=True):
  edge_list = []
  for key, value in question_dict.iteritems():
    scores = CalculateScores(value, structured_data_dict, False, scoring_default)
    edge_list.extend(GenerateGraphEdges(key, scores))
  return edge_list


def CalculateScores(question_set, structure_map, verbose=True,
                    scoring_default=True):
  if verbose:
    print '\n'
    print question_set
  dataframe = ConstructQuestionScoringMatrix(question_set, structure_map, scoring_default)
  if verbose:
    print dataframe
    print '\n'
  norm_dataframe = NormalizeDataFrame(dataframe)
  if verbose:
    print norm_dataframe
    print '\n'
  final_scores = GetMarkovScoresList(dataframe)
  if verbose:
    print final_scores
    print '\n'
  return final_scores

def getEndLevelWeights(graph):
  weights_list = []
  _crawlNetwork(graph,'ROOT', 1.0, weights_list)
  return sorted(weights_list, key=lambda tup: tup[1], reverse=True)


def _crawlNetwork(graph, node_name, weight, return_tuple_list):
  successors = graph.neighbors(node_name)
  if successors:
    for child_node in successors:
      _crawlNetwork(graph, child_node, weight*graph[node_name][child_node]['weight'], return_tuple_list)
  else:
    return_tuple_list.append((node_name, weight))
