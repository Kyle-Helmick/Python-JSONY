class val:
  def __init__(self, arr):
    self.arr = arr
    self.left = None
    self.mid = None
    self.right = None
    self.val = None
    self.type = "val"
    self.consume()
    
  def consume(self):
        
    if self.arr[0] == '"':
      value = ""
      value += self.arr.pop(0)
      while self.arr[0] != '"':
        value += self.arr.pop(0)
      value += self.arr.pop(0)
      self.val = value
      
    elif self.arr[0] == '[':
      self.val = array(self.arr)
      
    elif self.arr[0] == '{':
      self.val = json(self.arr)
      
    else:
      print("Error: Expected a '\"' | '[' | '{' to declare a value")
      
      exit(0)
    
class array_element:
  def __init__(self, arr):
    self.arr = arr
    
    self.left = None
    self.mid = None
    self.right = None
    self.type = "array_element"
    
    self.consume()
    
  def consume(self):
          
    temp = val(self.arr)
    
    if len(self.arr) == 0:
      print("Never found a closing bracket ']' for an array")
      exit(0)
    
    if self.arr[0] == ',':
      self.left = temp
      self.mid = self.arr.pop(0)
      self.right = array_element(self.arr)
      
    else:
      self.mid = temp
      
    return


class array:
  def __init__(self, arr):
    self.arr = arr
    
    self.left = None
    self.mid = None
    self.right = None
    self.type = "array"

    self.consume()
    
  def consume(self):
        
    if len(self.arr) < 2:
      print("Error: expected more than one character for array object")
      exit(0)
    
    # ===== This block consumes the first character
    self.left = self.arr.pop(0)
    if self.left != "[":
      print("Error: expected opening '[' square bracket")
      exit(0)
    
    # ===== This block handles the empty json object
    if self.arr[0] == ']':
      self.arr.pop(0)
      return

    # ===== This block calls consume on json element
    self.mid = array_element(self.arr)

    # ===== This block consumes the last character
    if len(self.arr) == 0:
      print("Error: expected closing ']' square bracket")
      exit(0)

    self.right = self.arr.pop(0)


class item:
  def __init__(self, arr):
    self.arr = arr
    
    self.left = None
    self.mid = None
    self.right = None
    self.type = "item"

    self.consume()
    
  def consume(self):
        
    if self.arr[0] != '"':
      print("Error: Expected \" to begin key declaration")
      exit(1)
    
    key = ""
    
    key += self.arr.pop(0)
    
    while self.arr[0] != '"':
      key += self.arr.pop(0)
      
    key += self.arr.pop(0)
    
    self.left = key
    
    self.mid = self.arr.pop(0)
    
    if self.mid != ":":
       print("Error: Expected : to seperate key and value")
        
    self.right = val(self.arr)
    
    return


class json_element:
  def __init__(self, arr):
    self.arr = arr
    
    self.left = None
    self.mid = None
    self.right = None
    self.type = "json_element"
    
    self.consume()
    
  def consume(self):
          
    temp = item(self.arr)
    
    if len(self.arr) == 0:
      print("Never found a closing bracket '}' for JSON object")
      exit(1)
    
    if self.arr[0] == ',':
      self.left = temp
      self.mid = self.arr.pop(0)
      self.right = json_element(self.arr)
      
    else:
      self.mid = temp
      
    return


class json:
  def __init__(self, arr):
    self.arr = arr
    
    self.left = None
    self.mid = None
    self.right = None
    self.type = "json"

    self.consume()
    
  def consume(self):
        
    if len(self.arr) < 2:
      print("Error: expected more than one character for JSON object")
      exit(0)
    
    # ===== This block consumes the first character
    self.left = self.arr.pop(0)
    if self.left != "{":
      print("Error: expected opening '{' curly brace")
      exit(0)
    
    # ===== This block handles the empty json object
    if self.arr[0] == '}':
      self.arr.pop(0)
      return

    # ===== This block calls consume on json element
    self.mid = json_element(self.arr)

    # ===== This block consumes the last character
    if len(self.arr) == 0:
      print("Error: expected closing '}' curly brace")
      exit(0)

    self.right = self.arr.pop(0)
    
class jsony_parser:

  def __init__(self, test_str):
    self.string = list(test_str)
    self.root = json(self.string)



test1 = '{"this":"that"}'
test2 = '{"this":"that","that":["one","two","three"]}'
test3 = '{"menu":{"id":"file","value":"File","popup":{"menuitem":[{"value":"New","onclick":"CreateNewDoc()"},{"value":"Open","onclick":"OpenDoc()"},{"value":"Close","onclick":"CloseDoc()"}]}}}'

#jsony_parser(test1)
tree2 = jsony_parser(test3)