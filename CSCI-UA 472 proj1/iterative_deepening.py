import sys
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

  indx=1;
  value_map ={}
  n = len(lines)
  while indx<n:
    parts =lines[indx].split()
    if len(parts)==0:
      indx+=1
      break
    ##print(target)
    vertex, val = parts
    ##print(vertex)
    ##print(val)
    value_map[vertex]=int(val)
    indx+=1

  neighbor = {v: set() for v in value_map.keys()}
  while indx<n:
    parts =lines[indx].split()
    a,b= parts
    neighbor[a].add(b)
    neighbor[b].add(a)
    indx+=1

  return target, value, value_map, neighbor

def work(target, value, value_map, neighbor):

  vertices = sorted(value_map.keys())
  n = len(vertices)
  solution = None


##start dfs execution
  def dfs(current_set, cur_index, depth_left):
    sum_val = sum(value_map[v] for v in current_set)
    if(sum_val>=target):
      return current_set, True
    elif(depth_left==0):
      return None, False
    foundSolution = None
    anySuccessor = False
    for i in range (cur_index, n):
      next_vertex = vertices[i]
      conflict = any(next_vertex in neighbor[v] for v in current_set)
      if conflict:
        continue
      anySuccessor = True
      current_set.add(next_vertex)
      if(len(current_set)>=depth_left):
        anySuccessor = True
      if value:
        print(" ".join(current_set), f"Value={sum(value_map[v] for v in current_set)}.")
      temp, successors = dfs(current_set, i+1, depth_left-1)
      if temp is not None:
        return temp, True
      current_set.remove(next_vertex)
    #print(anySuccessor)
    return None, anySuccessor
## done dfs execution


  for depth in range(1,n+1):
    if value:
      print(f"\nDepth={depth}")
    Final_set, has_successor = dfs(set(), 0, depth)
    ##print(has_successor)
    if Final_set is not None:
      print("\nFound solution"," ".join(Final_set), f"Value={sum(value_map[i] for i in Final_set)}")
      return
    elif not has_successor:
      print("\nNo solution found!!")
      return

  print("\nNo solution found")

def main():
    if len(sys.argv)!=2:
        print("wrong parameter numbers")
        sys.exit(1)
    input_file_name = sys.argv[1]
    target, value, value_map, neighbor = input_file(input_file_name)
    work(target, value, value_map, neighbor)

main()
