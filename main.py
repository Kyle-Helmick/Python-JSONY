class jsony_parser:

  def __init__(self):
    self.root = None

class json:
  def __init__(self):
    self.parent = None
    self.left = None
    self.mid = None
    self.right = None

  def consume(self, string):
    # string passed in should be longer than 1 character (safety check)
    # consume a character (should be a '{' )
    # call json_element.consume on the inside of the string and hopefully get a string of '}' back
    # consume the last character (should be a '}' )
    return

class json_element:
  def __init__(self):
    self.parent = None
    self.items = [] # Should be appending the instances of class item into this array

  def consume(self, string):
    # while there are characters to be consumed
      # if quotes call item.consume
      # if comma consume comma then call json_element again
      # else error
    return

class item:
  def __init__(self):
    self.parent = None

  def consume(self, string):
    # should check for string (but don't consume '"' ) and then call val.consume
      # if no string make error
    # should consume colon
    # should call val.consume
    return 

class array:
  def __init__(self):
    self.parent = None
  
  def consume(self, string):
    # should consume [
    # should call array_element.consume
    # should consume ]
    return

class array_element:
  def __init__(self):
    self.parent = None

  def consume(self, string):
    # while there are characters to be consumed
      # if quotes, bracket or brace call item.consume
      # if comma consume comma then call array_element.consume again
      # else error
    return

class val:
  def __init__(self):
    self.parent = None