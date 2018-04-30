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


class val:
  def __init__(self, arr, popped):
    self.arr = arr
    self.popped = popped

    self.left = None
    self.mid = None
    self.right = None
    self.val = None
    self.type = "val"
    self.consume()
    
  def consume(self):
        
    if self.arr[0] == '"':
      value = ""

      pop = self.arr.pop(0)
      value += pop
      self.popped.append(pop)

      while len(self.arr) > 0 and self.arr[0] != '"':
        pop = self.arr.pop(0)
        value += pop
        self.popped.append(pop)

      if len(self.arr) == 0:
        print("Error: Expected closing quote ")
        print_error(self.arr, self.popped)
        exit(1)

      pop = self.arr.pop(0)
      value += pop
      self.popped.append(pop)
      self.val = value
      
    elif self.arr[0] == '[':
      self.val = array(self.arr, self.popped)
      
    elif self.arr[0] == '{':
      self.val = json(self.arr, self.popped)
      
    else:
      print("Error: Expected a '' | '[' | '{' to declare a value")
      print_error(self.arr, self.popped)
      exit(1)
    
class array_element:
  def __init__(self, arr, popped):
    self.arr = arr
    self.popped = popped
    
    self.left = None
    self.mid = None
    self.right = None
    self.type = "array_element"
    
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
  def __init__(self, arr, popped):
    self.arr = arr
    self.popped = popped
    
    self.left = None
    self.mid = None
    self.right = None
    self.type = "array"

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
  def __init__(self, arr, popped):
    self.arr = arr
    self.popped = popped
    
    self.left = None
    self.mid = None
    self.right = None
    self.type = "item"

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
  def __init__(self, arr, popped):
    self.arr = arr
    self.popped = popped
    
    self.left = None
    self.mid = None
    self.right = None
    self.type = "json_element"
    
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
  def __init__(self, arr, popped):
    self.arr = arr
    self.popped = popped
    
    self.left = None
    self.mid = None
    self.right = None
    self.type = "json"

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

  def __init__(self, test_str):
    self.unpopped = list(test_str)
    self.popped = []
    self.root = json(self.unpopped, self.popped)



test1 = '{"this":"that"}'
test2 = '{"this":"that","that":["one","two","three"]}'
test3 = '{"text":"RT @PostGradProblem: In preparation for the NFL lockout, I will be spending twice as much time analyzing my fantasy baseball team during ...","truncated":"true","in_reply_to_user_id":"null","in_reply_to_status_id":"null","favorited":"false","source":"<a href=http://twitter.com/ rel=nofollow>Twitter for iPhone<\/a>","in_reply_to_screen_name":"null","in_reply_to_status_id_str":"null","id_str":"54691802283900928","entities":{"user_mentions":[{"indices":["3","19"],"screen_name":"PostGradProblem","id_str":"271572434","name":"PostGradProblems","id":"271572434"}],"urls":[],"hashtags":[]},"contributors":"null","retweeted":"false","in_reply_to_user_id_str":"null","place":"null","retweet_count":"4","created_at":"Sun Apr 03 23:48:36 +0000 2011","retweeted_status":{"text":"In preparation for the NFL lockout, I will be spending twice as much time analyzing my fantasy baseball team during company time. #PGP","truncated":"false","in_reply_to_user_id":"null","in_reply_to_status_id":"null","favorited":"false","source":"<a href=http://www.hootsuite.com rel=nofollow>HootSuite<\/a>","in_reply_to_screen_name":"null","in_reply_to_status_id_str":"null","id_str":"54640519019642881","entities":{"user_mentions":[],"urls":[],"hashtags":[{"text":"PGP","indices":["130","134"]}]},"contributors":"null","retweeted":"false","in_reply_to_user_id_str":"null","place":"null","retweet_count":"4","created_at":"Sun Apr 03 20:24:49 +0000 2011","user":{"notifications":"null","profile_use_background_image":"true","statuses_count":"31","profile_background_color":"C0DEED","followers_count":"3066","profile_image_url":"http://a2.twimg.com/profile_images/1285770264/PGP_normal.jpg","listed_count":"6","profile_background_image_url":"http://a3.twimg.com/a/1301071706/images/themes/theme1/bg.png","description":"","screen_name":"PostGradProblem","default_profile":"true","verified":"false","time_zone":"null","profile_text_color":"333333","is_translator":"false","profile_sidebar_fill_color":"DDEEF6","location":"","id_str":"271572434","default_profile_image":"false","profile_background_tile":"false","lang":"en","friends_count":"21","protected":"false","favourites_count":"0","created_at":"Thu Mar 24 19:45:44 +0000 2011","profile_link_color":"0084B4","name":"PostGradProblems","show_all_inline_media":"false","follow_request_sent":"null","geo_enabled":"false","profile_sidebar_border_color":"C0DEED","url":"null","id":"271572434","contributors_enabled":"false","following":"null","utc_offset":"null"},"id":"54640519019642880","coordinates":"null","geo":"null"},"user":{"notifications":"null","profile_use_background_image":"true","statuses_count":"351","profile_background_color":"C0DEED","followers_count":"48","profile_image_url":"http://a1.twimg.com/profile_images/455128973/gCsVUnofNqqyd6tdOGevROvko1_500_normal.jpg","listed_count":"0","profile_background_image_url":"http://a3.twimg.com/a/1300479984/images/themes/theme1/bg.png","description":"watcha doin in my waters?","screen_name":"OldGREG85","default_profile":"true","verified":"false","time_zone":"Hawaii","profile_text_color":"333333","is_translator":"false","profile_sidebar_fill_color":"DDEEF6","location":"Texas","id_str":"80177619","default_profile_image":"false","profile_background_tile":"false","lang":"en","friends_count":"81","protected":"false","favourites_count":"0","created_at":"Tue Oct 06 01:13:17 +0000 2009","profile_link_color":"0084B4","name":"GG","show_all_inline_media":"false","follow_request_sent":"null","geo_enabled":"false","profile_sidebar_border_color":"C0DEED","url":"null","id":"80177619","contributors_enabled":"false","following":"null","utc_offset":"-36000"},"id":"54691802283900930","coordinates":"null","geo":"null"}'

print("test1")
jsony_parser(test1)
print("test2")
jsony_parser(test2)
print("test3")
jsony_parser(test3)