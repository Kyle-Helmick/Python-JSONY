def print_error(unpopped, popped):
  if len(popped) >= 10:
    print("".join(str(x) for x in popped[-10:]), end='')
  else:
    print("".join(str(x) for x in popped), end='')
  print(' ? ', end='')
  if len(unpopped) >= 10:
    print("".join(str(x) for x in unpopped[:10]))
  else:
    print("".join(str(x) for x in unpopped))


class num:
    def __init__(self, arr, popped):
        self.arr = arr
        self.popped = popped
        self.val = None
        self.type = "number"
        self.valid_num = ['0','1','2','3','4','5','6','7','8','9']
        self.consume()

    def consume(self):
        #Adding the first character, could include -
        pop = self.arr.pop(0)
        value=pop
        self.popped.append(pop)
        decimal = False

        #Looping to find the rest of the number
        while(len(self.arr) > 0 and (self.arr[0] in self.valid_num or self.arr[0] == '.')):
          #Checking if there's too many .
          if(decimal and self.arr[0] == '.'):
            print("Error: Only one decimal allowed in numbers")
            print_error(self.arr,self.popped)
            exit(1)
          pop = self.arr.pop(0)
          value += pop
          self.popped.append(pop)
          if pop == '.':
            decimal=True

        #Checking if we're at the end of the string
        if len(self.arr) == 0:
          print("Error: Expected more characters")
          print_error(self.arr, self.popped)
          exit(1)
        #Updating variables
        self.val = float(value)


class val:

  '''
  Arguments:
    arr: This should be a pointer (mutable object) to the string that the parser is parsing.

    popped: This should be a pointer (mutable object) to the string that the parser has parsed.

  Attributes:
    arr: A list of the characters that have been popped within the parser
    
    popped: A list of the characters that have been successfully popped

    left:

    mid:

    right:

    valid:

  Functions:


  Returns:
    None
  '''

  def __init__(self, arr, popped):
    self.arr = arr
    self.popped = popped
    self.left = None
    self.mid = None
    self.right = None
    self.val = None
    self.valid_num = ['0','1','2','3','4','5','6','7','8','9']
    self.consume()

  '''Parsing for a string'''
  def string(self):
    #Getting the first quote
    value = ""
    pop = self.arr.pop(0)
    value += pop
    self.popped.append(pop)

    #Adding the rest of the string
    while len(self.arr) > 0 and self.arr[0] != '"':
      pop = self.arr.pop(0)
      value += pop
      self.popped.append(pop)

    #Checking for end of string
    if len(self.arr) == 0:
      print("Error: Expected closing quote ")
      print_error(self.arr, self.popped)
      exit(1)

    #Updating variables
    pop = self.arr.pop(0)
    value += pop
    self.popped.append(pop)
    self.val = value

  '''Checking for true'''
  def true_test(self):
    #Getting the first character
    val = self.arr.pop(0)
    self.popped.append(val)
    #Getting the rest
    for _ in range(3):
      if(len(self.arr)>0):
        pop = self.arr.pop(0)
        self.popped.append(pop)
        val += pop
      else:
        print("Error: Expected true, got: ", val)
        print_error(self.arr, self.popped)
        exit(1)
    #Checking if it was actually true
    if val == 'true':
      self.value = True
    else:
      print("Error: Expected true, got: ", val)
      print_error(self.arr,self.popped)
      exit(1)

  '''Checking for false'''
  def false_test(self):
    #Getting the first character
    val=self.arr.pop(0)
    self.popped.append(val)
    for _ in range(4):
      #Checking for end of string
      if(len(self.arr)>0):
        pop = self.arr.pop(0)
        self.popped.append(pop)
        val += pop
      else:
        print("Error: Expected  false, got: ", val)
        print_error(self.arr, self.popped)
        exit(1)
    #Setting it to false
    if val == 'false':
      self.value = False
    else:
      print("Error: Expected false, got: ", val)
      print_error(self.arr,self.popped)
      exit(1)

  '''Checking for null'''
  def null_test(self):
    val = self.arr.pop(0)
    self.popped.append(val)
    for _ in range(3):
      #Checking for the end of string
      if(len(self.arr)>0):
        pop = self.arr.pop(0)
        self.popped.append(pop)
        val += pop
      else:
        print("Error:  Expected null, got: ", val)
        print_error(self.arr,self.popped)
        exit(1)
    #Updating variables
    if val == 'null':
      self.value = None
    else:
      print("Error: Expected null, got: ", val)
      print_error(self.arr,self.popped)
      exit(1)

  def consume(self):
    #String
    if self.arr[0] == '"':
      self.string()
    #Array
    elif self.arr[0] == '[':
      self.val = array(self.arr, self.popped)
    #JSON Object
    elif self.arr[0] == '{':
      self.val = json(self.arr, self.popped)
    #Numbers
    elif self.arr[0] in self.valid_num or self.arr[0] == '-':
      self.val = num(self.arr, self.popped)
    #Boolean True
    elif self.arr[0] == 't':
      self.true_test()
    #Boolean False
    elif self.arr[0] == 'f':
      self.false_test()
    #NULL Value
    elif self.arr[0] == 'n':
      self.null_test()
    #If nothing matches, we don't support the type
    else:
      print("Error: Expected a '' | '[' | '{' to declare a value")
      print_error(self.arr, self.popped)
      exit(1)

class array_element:

  '''
  Arguments:
    arr: This should be a pointer (mutable object) to the string that the parser is parsing.
    
    popped: This should be a pointer (mutable object) to the string that the parser has parsed.

  Attributes:
    arr: A list of the characters that have been popped within the parser

    popped: A list of the characters that have been successfully popped

    left: Should contain either None, if there is only 1 item in this array, or a val object if multiple items

    mid: Should contain either val object, if there is only 1 item in this array, or a ',' charecter if multiple items

    right: Should contain either None, if there is only 1 item in this array, or a array_element object if multiple items

  Functions:
    consume: This function consumes brackets and makes the json_element object to go into self.mid

  Returns:
    None
  '''

  def __init__(self, arr, popped):
    self.arr = arr
    self.popped = popped

    self.left = None
    self.mid = None
    self.right = None

    self.consume()

  def consume(self):

    temp = val(self.arr, self.popped)

    if len(self.arr) == 0:
      print("Never found a closing bracket ']' for an array")
      print_error(self.arr, self.popped)
      exit(1)

    if self.arr[0] == ',':
      self.left = temp

      pop = self.arr.pop(0)
      self.popped.append(pop)
      self.mid = pop

      self.right = array_element(self.arr, self.popped)

    else:
      self.mid = temp

    return


class array:

  '''
  Arguments:
    arr: This should be a pointer (mutable object) to the string that the parser is parsing.

    popped: This should be a pointer (mutable object) to the string that the parser has parsed.

  Attributes:
    arr: A list of the characters that have been popped within the parser
    
    popped: A list of the characters that have been successfully popped

    left: Should contain the character '['

    mid: Should contain an array_element object

    right: Should contain the character ']'

  Functions:
    consume: This function consumes brackets and makes the array_element object to go into self.mid

  Returns:
    None
  '''

  def __init__(self, arr, popped):
    self.arr = arr
    self.popped = popped

    self.left = None
    self.mid = None
    self.right = None

    self.consume()

  def consume(self):

    if len(self.arr) < 2:
      print("Error: expected more than one character for array object")
      print_error(self.arr, self.popped)
      exit(1)

    # ===== This block consumes the first character
    pop = self.arr.pop(0)
    self.left = pop
    self.popped.append(pop)
    if self.left != "[":
      print("Error: expected opening '[' square bracket")
      print_error(self.arr, self.popped)
      exit(1)

    # ===== This block handles the empty json object
    if self.arr[0] == ']':
      pop = self.arr.pop(0)
      self.right = pop
      self.popped.append(pop)
      return

    # ===== This block calls consume on json element
    self.mid = array_element(self.arr, self.popped)

    # ===== This block consumes the last character
    if len(self.arr) == 0 or self.arr[0] != ']':
      print("Error: expected closing ']' square bracket")
      print_error(self.arr, self.popped)
      exit(1)

    pop = self.arr.pop(0)
    self.popped.append(pop)
    self.right = pop


class item:
 

  '''
  Arguments:
    arr: This should be a pointer (mutable object) to the string that the parser is parsing.
    
    popped: This should be a pointer (mutable object) to the string that the parser has parsed.

  Attributes:
    arr: A list of the characters that have been popped within the parser

    popped: A list of the characters that have been successfully popped

    left: Should contain the Key to the items Key:value pair - this will be a string 

    mid: Should be the charecter ':'

    right: Should contain the val object

  Functions:
    consume: This function consumes brackets and makes the json_element object to go into self.mid

  Returns:
    None
  '''


   def __init__(self, arr, popped):
    self.arr = arr
    self.popped = popped

    self.left = None
    self.mid = None
    self.right = None

    self.consume()

  def consume(self):

    if self.arr[0] != '"':
      print("Error: Expected  to begin key declaration")
      print_error(self.arr, self.popped)
      exit(1)

    key = ""
    pop = self.arr.pop(0)
    key += pop
    self.popped.append(pop)

    while self.arr[0] != '"':
      pop = self.arr.pop(0)
      key += pop
      self.popped.append(pop)

    pop = self.arr.pop(0)
    key += pop
    self.popped.append(pop)

    self.left = key

    if self.arr[0] != ":":
       print("Error: Expected : to seperate key and value")
       print_error(self.arr, self.popped)
       exit(1)

    pop = self.arr.pop(0)
    self.mid = pop
    self.popped.append(pop)

    self.right = val(self.arr, self.popped)

    return


class json_element:

  '''
  Arguments:
    arr: This should be a pointer (mutable object) to the string that the parser is parsing.

    popped: This should be a pointer (mutable object) to the string that the parser has parsed.

  Attributes:
    arr: A list of the characters that have been popped within the parser
    
    popped: A list of the characters that have been successfully popped

    left: If the json_element only contains a single item this will be empty
          If the json element contains multiple items this will be an item object

    mid: If the json_element only contains a single item this will be an item object
         If the json_element contains multiple items this will be the character ','

    right: If the json_element only contains a single item this will be empty
           If the json_element contains multiple items this will be a json_element object

  Functions:
    consume: This function creates an item object and then decides whether there are multiple items
             in the json object

  Returns:
    None
  '''

  def __init__(self, arr, popped):
    self.arr = arr
    self.popped = popped

    self.left = None
    self.mid = None
    self.right = None

    self.consume()

  def consume(self):

    temp = item(self.arr, self.popped)

    if len(self.arr) == 0:
      print("Never found a closing bracket '}' for JSON object")
      print_error(self.arr, self.popped)
      exit(1)

    if self.arr[0] == ',':
      self.left = temp

      pop = self.arr.pop(0)
      self.mid = pop
      self.popped.append(pop)

      self.right = json_element(self.arr, self.popped)

    else:
      self.mid = temp

    return


class json:

  '''
  Arguments:
    arr: This should be a pointer (mutable object) to the string that the parser is parsing.
    
    popped: This should be a pointer (mutable object) to the string that the parser has parsed.

  Attributes:
    arr: A list of the characters that have been popped within the parser

    popped: A list of the characters that have been successfully popped

    left: Should contain the character '{'

    mid: Should contain a json_element object

    right: Should contain the character '}'

  Functions:
    consume: This function consumes braces and makes the json_element object to go into self.mid

  Returns:
    None
  '''

  def __init__(self, arr, popped):
    self.arr = arr
    self.popped = popped

    self.left = None
    self.mid = None
    self.right = None

    self.consume()

  def consume(self):

    if len(self.arr) < 2:
      print("Error: expected more than one character for JSON object")
      exit(1)

    # ===== This block consumes the first character
    pop = self.arr.pop(0)
    self.left = pop
    self.popped.append(pop)
    if self.left != "{":
      print("Error: expected opening '{' curly brace")
      print_error(self.arr, self.popped)
      exit(1)

    # ===== This block handles the empty json object
    if self.arr[0] == '}':
      pop = self.arr.pop(0)
      self.right = pop
      self.popped.append(pop)
      return

    # ===== This block calls consume on json element
    self.mid = json_element(self.arr, self.popped)

    # ===== This block consumes the last character
    if len(self.arr) == 0:
      print("Error: expected closing '}' curly brace")
      print_error(self.arr, self.popped)
      exit(1)

    pop = self.arr.pop(0)
    self.right = pop
    self.arr.append(pop)

    if self.right != '}':
      print("Error: expected closing '}' curly brace")
      print_error(self.arr, self.popped)
      exit(1)

class jsony_parser:

  '''
  Arguments:
    test_str: A single line string that has the JSON format. There should be no whitespace
              inbetween JSON special characters. There shouldn't be any escaped characters within
              strings as values or keys either.

  Attributes:
    arr: A list of the characters that have been popped within the parser

    popped: A list of the characters that have been successfully popped

    root: The root object in our "tree" structure for the parsed object

  Returns:
    None
  '''

  def __init__(self, test_str):
    self.arr = list(test_str)
    self.popped = []
    self.root = json(self.arr, self.popped)

