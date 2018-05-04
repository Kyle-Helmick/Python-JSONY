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
  
  '''
  Arguments:
    arr: This should be a pointer (mutable object) to the string that the parser is parsing.

    popped: This should be a pointer (mutable object) to the string that the parser has parsed.

  Attributes:
    arr: A list of the characters that have been popped within the parser
    
    popped: A list of the characters that have been successfully popped

    val: This should hold a float after self.consume is done

    valid_num: This is an array of valid digits.

  Functions:
    consume: This pops values off of self.arr only allowing for digits or digits and a single
             decimal point

  Returns:
    None
  '''

  def __init__(self, arr, popped):
      self.arr = arr
      self.popped = popped
      self.val = None
      self.valid_num = ['0','1','2','3','4','5','6','7','8','9']
      self.consume()

  def consume(self):
      #Adding the first character, could include -
      pop = self.arr.pop(0)
      self.val = pop
      self.popped.append(pop)
      decimal = False

      #Looping to find the rest of the number
      while(len(self.arr) > 0 and (self.arr[0] in self.valid_num or self.arr[0] == '.')):
        #Checking if there's too many '.'s
        if(decimal and self.arr[0] == '.'):
          print("Error: Only one decimal allowed in numbers")
          print_error(self.arr,self.popped)
          exit(1)
        pop = self.arr.pop(0)
        self.val += pop
        self.popped.append(pop)
        if pop == '.':
          decimal=True

      #Checking if we're at the end of the string
      if len(self.arr) == 0:
        print("Error: Expected more characters")
        print_error(self.arr, self.popped)
        exit(1)
      #Updating variables
      self.val = float(self.val)

class val:

  '''
  Arguments:
    arr: This should be a pointer (mutable object) to the string that the parser is parsing.

    popped: This should be a pointer (mutable object) to the string that the parser has parsed.

  Attributes:
    arr: A list of the characters that have been popped within the parser
    
    popped: A list of the characters that have been successfully popped

    left: This should stay empty

    mid: This should become one of possible values, str | array | json | num | true | false | null

    right: This should stay empty

    valid_num: This is an array of valid digits.

  Functions:
    string_consume: This functio.n will try to consume a string and error out if quotes are missing
                    in any way

    bool_consume: This function will try to consume a boolean and error out if the boolean is
                  mispelled or not a boolean.

    consume: This function decides which val the parser should attemp to consume.

  Returns:
    None
  '''

  def __init__(self, arr, popped):
    self.arr = arr
    self.popped = popped

    self.left = None
    self.mid = ""
    self.right = None
    self.valid_num = ['0','1','2','3','4','5','6','7','8','9']
    self.consume()

  def string_consume(self):
    #Getting the first quote
    pop = self.arr.pop(0)
    self.mid += pop
    self.popped.append(pop)

    #Adding the rest of the string
    while len(self.arr) > 0 and self.arr[0] != '"':
      pop = self.arr.pop(0)
      self.mid += pop
      self.popped.append(pop)

    #Checking for end of string
    if len(self.arr) == 0:
      print("Error: Expected closing quote ")
      print_error(self.arr, self.popped)
      exit(1)

    #Updating variables
    pop = self.arr.pop(0)
    self.mid += pop
    self.popped.append(pop)

  def bool_consume(self):
    bools = ['false', 'true', 'null']
    map_ = [False, True, None]

    temp = ""
    for bool_ in bools:
      if self.arr[0] == bool_[0]:
        pop = self.arr.pop(0)
        temp += pop
        self.popped.append(pop)
        for char in bool_[1:]:
          if self.arr[0] == char:
            pop = self.arr.pop(0)
            temp += pop
            self.popped.append(pop)
          else:
            print("Error: Expected bool, got: ", temp)
            print_error(self.arr, self.popped)
            exit(1)
        if temp in bools:
          self.mid = map_[bools.index(temp)]

    if temp == "":
      print("Error: Expected bool indicator 't' | 'f' | 'n'")
      print_error(self.arr, self.popped)
      exit(1)

  def consume(self):
    #String
    if self.arr[0] == '"':
      self.string_consume()

    #Array
    elif self.arr[0] == '[':
      self.mid = array(self.arr, self.popped)

    #JSON Object
    elif self.arr[0] == '{':
      self.mid = json(self.arr, self.popped)

    #Numbers
    elif self.arr[0] in self.valid_num or self.arr[0] == '-':
      self.mid = num(self.arr, self.popped)
    
    #Boolean True
    elif self.arr[0] == 't' or self.arr[0] == 'f' or self.arr[0] == 'n':
      self.bool_consume()
    
    #If nothing matches, we don't support the type
    else:
      print("Error: Expected a '\"' | '[' | '{' | '0-9' | '-' | 't' | 'f' | 'n' to declare a value")
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

    left: If the array_element only contains a single val this will be empty
          If the array_element contains multiple vals this will be a val object

    mid: If the array_element only contains a single val this will be an val object
         If the array_element contains multiple items this will be the character ','

    right: If the array_element only contains a single val this will be empty
           If the array_element contains multiple vals this will be an array_element object

  Functions:
    consume: This function consumes characters to define vals and array elements

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

    right: Should contain a val object

  Functions:
    consume: This function consumes quotes and makes the val object to go into self.right

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
    self.popped.append(pop)

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

test = '{"This":"that","this":100,"this":-100,"this":-1.0,"this":1.0,"this":false,"this":true,"this":null}'
jsony_parser(test)