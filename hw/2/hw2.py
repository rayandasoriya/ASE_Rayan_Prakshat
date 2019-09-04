import re
import zipfile

def compiler(x):
  "return something that can compile strings of type x"
  try: int(x); return  int 
  except:
    try: float(x); return  float
    except ValueError: return str

def string(s):
  "read lines from a string"
  for line in s.splitlines(): 
	  yield line

def file(fname):
  "read lines from a fie"
  with open(fname) as fs:
      for line in fs: yield line

def zipped(archive,fname):
  "read lines from a zipped file"
  with zipfile.ZipFile(archive) as z:
     with z.open(fname) as f:
        for line in f: yield line

def rows(src, 
         sep=     ",",
         doomed = r'([\n\t\r ]|#.*)'):
  "convert lines into lists, killing whitespace and comments"
  for line in src:
    line = line.strip()
    line = re.sub(doomed, '', line)
    if line:
      yield line.split(sep)
    else:
      yield line

question_check = []
def cells(src):
  "convert strings into their right types"
  oks = None
  prev = 0
  for n,cells in enumerate(src):    
    if not cells:
      continue
    if not prev:
      prev = len(cells)
    if prev!= len(cells):
      print("E> Skipping line ", n+1)
      continue
    # print(cells)
    if n==0:
      for cell in range(len(cells)):
        if '?' in cells[cell]:
          question_check.append(cell)
      new_arr = []
      for i in range(len(cells)):
        if i not in question_check:
          new_arr.append(cells[i])
      yield new_arr
    else:
        new_arr = []
        for cell in range(len(cells)):
          if '?' in cells[cell]:
            cells[cell] = 0
        # new_arr = []
        for i in range(len(cells)):
            if i not in question_check:
              new_arr.append(cells[i])  
        oks = oks or [compiler(cell) for cell in new_arr]
        yield [f(cell) for f,cell in zip(oks,new_arr)]



if __name__=="__main__":
  s="""$cloudCover, $temp, ?$humid, <wind,  $playHours
  100,        68,    80,    0,    3   # comments
  0,          85,    85,    0,    0

  0,          80,    90,    10,   0
  60,         83,    86,    0,    4
  100,        70,    96,    0,    3
  100,        65,    70,    20,   0
  70,         64,    65,    15,   5
  0,          72,    95,    0,    0
  0,          69,    70,    0,    4
  ?,          75,    80,    0,    ?
  0,          75,    70,    18,   4
  60,         72,
  40,         81,    75,    0,    2
  100,        71,    91,    15,   0
  """
  ans = []
  for lst in fromString(s):
	  print(lst)
    #ans.append(lst)
  #print(ans)