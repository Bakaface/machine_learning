import re
import os
import pprint

pp = pprint.PrettyPrinter()

def convert_file(filepath, attributes=None, answers=None, values=None,
                 answer_column_index=-1, id_column_index=None, regexp=r",\s*|\s*"):
  elements = []
  answer_column_index_trigger = False
  with open(filepath) as file:
    for line in [line.strip() for line in file.readlines()]:
      numbers = re.split(regexp, line)
      if answer_column_index < 0 and not answer_column_index_trigger:
        answer_column_index += len(numbers)
        answer_column_index_trigger = True
      element = {}
      element['object'] = {}
      for index, number in enumerate(numbers):
        if index == id_column_index:
          pass
        elif index == answer_column_index:
          element['answer'] = f"ans{number}" if not answers else answers[number]
        else:
          element['object'][
            f"attr{index}" if not attributes else attributes[index]
          ] = f"val{number}" if not values else values[number]
      elements.append(element)
  return(elements)

if __name__ == "__main__":
  pp.pprint(
    convert_file(
      f"{os.path.dirname(__file__)}/../data/balance-scale-small.data",
      attributes=['', 'a1', 'a2', 'a3', 'a4'],
      values={'1': 'v1', '2': 'v2', '3': 'v3', '4': 'v4', '5': 'v5'},
      answer_column_index=0))