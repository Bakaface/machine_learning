from lib.node import Node
from statistics import mode
from functools import reduce
from math import log2
from os import path

import json
import pprint

pp = pprint.PrettyPrinter()

class ID3(object):
  def __init__(self, node):
    self.node = node

  def learn(self, traning_sample):
    self.__learn(self.node, traning_sample)
    return

  def print_tree(self):
    self.node.print()

  def run(self):
    self.__step(self.node)

  @staticmethod
  def __step(node):
    if node.is_end_node():
      print(f"Answer: {node.answer}")
      return
    choices = list(node.children.keys())
    print(f"{node.attribute}? {choices}")
    answer = input()
    for i in range(0, len(choices)):
      if int(answer) == i + 1:
        ID3.__step(node.children[choices[i]])

  @staticmethod
  def __gain(training_sample, attributes, answers):
    """returns title of attribute with maximum amount of information gain"""
    sample_gains = {}
    for attribute, values in attributes.items():
      #all answers of sample
      sample_answers = [element['answer'] for element in training_sample]
      #count enthropy for root node in sample
      sample_enthropy = sum(
          p * -1 * log2(p)
          for p in [sample_answers.count(answer)/len(sample_answers) for answer in answers]
          if p > 0
        )
      #count subtrahend of gain formula (Enthtopy(S) - sum(Sv * Enthtopy(Sv)/S)))
      gain_subtrahend = 0
      for value in values:
        #all answers of part of a sample with matching value
        value_answers = [
          element['answer'] 
          for element in training_sample 
          if element['object'][attribute] == value
        ]
        #count enthropy for one of possible child nodes
        value_enthropy = sum(
          p * -1 * log2(p)
          for p in [value_answers.count(answer)/len(value_answers) for answer in answers]
          if p > 0
        )
        gain_subtrahend += len(value_answers) * value_enthropy / len(sample_answers)
      sample_gains[attribute] = sample_enthropy - gain_subtrahend
    return max(sample_gains, key=sample_gains.get)

  @staticmethod
  def __learn(node, training_sample):
    #setting number or objects passed through current node
    node.training_objects_count = len(training_sample)
    #forming list of all actual answers
    answers = list(set([element['answer'] for element in training_sample]))
    for answer in answers:
      if all([sample['answer'] == answer for sample in training_sample]):
        node.answer = answer
        return
    #forming list of values for each attribute
    attributes = {
      attribute: list(
        set(
          map(
            lambda element: element['object'][attribute], 
            training_sample
          )
        )
      )
      for attribute in training_sample[0]['object'].keys()
    }
    attribute = ID3.__gain(training_sample, attributes, answers)
    node.attribute = attribute
    for value in attributes[attribute]:
      new_node = Node()
      node.add_child(new_node, value)
      new_traning_sample = [sample for sample in training_sample if sample['object'][attribute] == value]
      ID3.__learn(new_node, new_traning_sample)
    return

  

if __name__ == "__main__":
  training_sample = json.loads(open('data/sample.json').read())
  node = Node()
  id3 = ID3(node)
  id3.learn(training_sample)
  id3.print_tree()
  id3.run()