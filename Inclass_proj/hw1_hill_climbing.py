import sys
import random

def input_file(file_name):
  lines = []
  with open(file_name) as ip:
    for line in ip:
      if line:
        lines.append(line)

  fst_line=lines[0].split()
  target = int(fst_line[0])
  if(fst_line[1]=='V'):
    value =True
  else:
    value =False
  restart_num = int(fst_line[2])
  indx=1;
  value_map ={}
  n = len(lines)
  while indx<n:
    parts =lines[indx].split()
    if len(parts)==0:
      indx+=1
      break
    vertex, val = parts
    ##print( vertex)
    ##print( val)
    value_map[vertex]=int(val)
    indx+=1

  neighbor = {v: set() for v in value_map.keys()}
  while indx<n:
    parts =lines[indx].split()
    a,b= parts
    neighbor[a].add(b)
    neighbor[b].add(a)
    indx+=1
  return target, value, value_map, neighbor, restart_num

def compute_value_error(target, value_map, neighbor, current_set):
  value = sum(value_map[v] for v in current_set)
  var = 0
  for v in current_set:
    for n in neighbor[v]:
      if n in current_set:
        var=min(value_map[v], value_map[n])
  error = max(0, target-value)+int(var)
  return value, error

def hill_climbing(target, value, value_map, neighbor, restart_num):
  vertices = sorted(value_map.keys())
  n = len(vertices)
  #print("N:::",n)
  for i in range (0,restart_num):
    #print(n)
    rand_range= random.randint(0,len(vertices))
    current_set = set()
    for i in range(0,rand_range):
      rand_index = random.randint(0,len(vertices)-1)
      current_set.add(vertices[rand_index])
    print("Randomly chosen start state: ", " ".join(current_set))
    value, error = compute_value_error(target, value_map, neighbor, current_set)
    print(" ".join(current_set), "Value:",value, "Error:", error)
    if error ==0:
      print("Solution found", " ".join(current_set), "Value:",value)
      return
    min_error = error
    #flag = False
    min_set=current_set.copy()
    #for i in range(0,2):
    while True:
      flag = False
      print("Neighbors")
      current_set=min_set
      ##add a vertex
      #print(i, current_set)
      for v in value_map.keys():
        if v not in current_set:
          temp_set = current_set.copy()
          temp_set.add(v)
          temp_value, temp_error = compute_value_error(target, value_map, neighbor, temp_set)
          print(" ".join(temp_set), "Value:",temp_value, "Error:", temp_error)
          if temp_error<min_error:
            min_error = temp_error
            min_set = temp_set.copy()
            value = temp_value
            flag = True
      ## delete a vertex
      for v in current_set:
        temp_set = set()
        for n in current_set:
          if v!=n:
            temp_set.add(n)
        temp_value, temp_error = compute_value_error(target, value_map, neighbor, temp_set)
        print(" ".join(temp_set), "Value:",temp_value, "Error:", temp_error)
        if(temp_error<min_error):
          min_error = temp_error
          min_set = temp_set.copy()
          value = temp_value
          flag = True

      if min_error ==0:
        print("Solution found", " ".join(min_set), "Value:",value)
        return
      if not flag:
        print("\nSearch failed\n")
        break
      print("Move to", " ".join(min_set), "Value:", value, "Error:", min_error, "\n")


def main():
    if len(sys.argv)!=2:
        print("wrong parameter numbers")
        sys.exit(1)
    input_file_name = sys.argv[1]
    target, value, value_map, neighbor, restart_num = input_file(input_file_name)
    hill_climbing(target, value, value_map, neighbor, restart_num)
if __name__ == '__main__':
    main()
