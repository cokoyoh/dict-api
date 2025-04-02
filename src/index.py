print(f'Data to test...')

def trial():
  x = 3
  print(f'x = {x}')
  
trial()

class Trial:
  def __init__(self):
    print(f'Initializiing class...')
  
  def build(self):
    print(f'Class fully initiated...')
  
obj = Trial()
obj.build()
