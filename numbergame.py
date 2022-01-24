# Alternative implementation of
# https://github.com/codewithbas/yaml-lisp-python
# https://bas.codes/posts/yaml-lisp-number-guessing

import yaml

class YamlIsAProgrammingLanguage:

  # Define all the functions in our YAML programming language:

  def repeat(self, times, expr):
    for i in range(0, times):
      try:
        self.call(expr)
      except BreakException:
        break

  def say(self, string):
    print(string)

  def read(self, var):
    self.vars[var] = input("Enter a value: ")

  def if_(self, cond, then, else_):
    if self.call(cond):
      self.call(then)
    else:
      self.call(else_)

  def eq(self, x, y):
    return str(self.call(x)) == str(self.call(y))

  def get(self, var):
    return self.vars.get(var, None)

  def break_(self, _):
    raise BreakException


  # The class constructor initializes the runtime state:
  def __init__(self):
    self.vars = {}

  # The PyYAML loader _is_ the compiler!
  def compile(self, program):
    loader = yaml.FullLoader
    yaml.add_multi_constructor('', type(self).yaml_constructor, loader)
    self.ast = yaml.load(program, loader)
    return self

  # Run the program by just calling the AST:
  def run(self):
    self.call(self.ast)

  # Call a method in the AST:
  def call(self, block):
    if type(block) == tuple:
      block = [ block ]
    if type(block) != list:
      return block

    for stmt in block:
      (name, expr) = stmt
      method = getattr(self, name)
      if type(expr) != list:
        expr = [expr]
      value = method(*expr)

    return value

  # This is how we can use YAML `!foo` as function names:
  @staticmethod
  def yaml_constructor(loader, name, node):
    name = name[1:]
    function_name = names.get(name, name)

    if isinstance(node, yaml.ScalarNode):
      function_args = loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
      function_args = loader.construct_sequence(node)
    elif isinstance(node, yaml.MappingNode):
      function_args = loader.construct_mapping(node)

    return (function_name, function_args)

names = {
  '==': 'eq',
  'if': 'if_',
  'break': 'break_',
}

class BreakException(Exception): pass

program = """
- !repeat
  - 3
  - - !say Please guess a number
    - !read number
    - !if
      - !== [ !get number, 777 ]
      - - !say That was correct!
        - !break
      - !say Try again!
"""

YamlIsAProgrammingLanguage().compile(program).run()
