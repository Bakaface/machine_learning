class Node(object):
  def __init__(self):
    self.attribute = None
    self.answer = None
    self.children = {}
    self.indent = '..'
    self.training_objects_count = 0

  def add_child(self, node, key):
    self.children[key] = node

  def is_end_node(self):
    return len(self.children) == 0

  def print(self):
    self.__print(self.indent, 'ROOT', self.attribute, self.answer)

  def __print(self, indent, key, attribute, answer):
    if self.is_end_node():
      print(indent + f"[(-{key}->), ({answer})] {self.training_objects_count} o.")
    else:
      print(indent + f"[(-{key}->), {attribute}] {self.training_objects_count} o.")
      for key, node in self.children.items():
        node.__print(indent + self.indent, key, node.attribute, node.answer)