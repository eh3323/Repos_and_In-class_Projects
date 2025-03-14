# Implementation of basic DPLL algorithm
# atoms are integers 1...N
# literals are either positive or negative atom
# a clause is a set of literals

# The set of clauses is implemented as a list, because Python does not support sets of sets.
# The bindings is implemented as an array of size nAtoms (the number of atoms) where
# bindings[i] == 1 if atom i is bound to True
#               -1 if atom i is bound to False
#                0 if atom i is unbound

import numpy as np  # only used in creating random examples
global nAtoms  # number of propositional atoms + 1 (because Python uses zero-based indexing)
global debug   # Boolean flag for printing trace information
debug=False  
global strategy # Boolean flag to choose strategy in choosing atom to split on.
                # True for "clever" strategy, False for just choosing first unbound atom

strategy = True

# superroutine: initializes bindings then calls the recursive DPLL.
def DPLLTop(clauses):
    global nAtoms
    nAtoms = 0
    for c in clauses:
        for lit in c:
            nAtoms = max(nAtoms,abs(lit))
    nAtoms += 1       # because Python uses 0-based indexing
    found, bindings = DPLL(clauses,[0]*nAtoms,0)
    return found, bindings

# Recursive call to DPLL
# depth is the depth of recursion. This is just there as defensive programming, in case some
# bug would otherwise give rise to an infinite depth recursion

def DPLL(clauses, bindings,depth):
    global nAtoms
    if depth > nAtoms:                    # Just to be on the safe side
        print("Recursion is too deep. Something is wrong")
        return
    easy = True
    while easy:
        if len(clauses) == 0:            # clauses is the empty set
            if debug:
                print("\nSuccess! ",bindings)
            return True, bindings
        if set() in clauses:              # the empty clause has been derived
            if debug:
                print("\nFailure. Backtracking")
            return False, bindings      
        easy, clauses, bindings = SingletonClause(clauses,bindings)
        if not easy:
            easy, clauses, bindings = PureLiteral(clauses,bindings)
    if strategy:
        p,sign = ChooseUnbound(clauses)
    else:
        p = 1+bindings[1:].index(0) # first unbound atom
        sign = 1
    clausesSaved, bindingsSaved = CopyClauses(clauses,bindings)
    if debug:
        print("\nNo easy cases. Splitting on ", p, ". Sign = ", sign)
    clauses, bindings = Propagate(clauses,bindings,p,sign)
    if debug:
        print("\n\nNew set:")
        for c in clauses:
             print(c)
        print("\n")
    success, bindings = DPLL(clauses,bindings,depth+1)
    if success:
        return True, bindings
    clauses, bindings = Propagate(clausesSaved,bindingsSaved,p,-sign)
    return DPLL(clauses,bindings,depth+1)

# find a singleton clause and propagate the corresponding assignment
def SingletonClause(clauses,bindings):    
    global debug
    for clause in clauses:
        if len(clause) == 1:
            lit, = clause
            p = abs(lit)
            sign = lit//p
            if debug:
               print("Singleton Clause", clause)
            clauses, bindings = Propagate(clauses,bindings,p,sign)
            return True, clauses, bindings
    return False, clauses, bindings

# find a pure literal, and propagate the corresponding assignment
def PureLiteral(clauses,bindings):
    global nAtoms
    signs = [set() for i in range(nAtoms)]
    for c in clauses:
        for lit in c:
            i = abs(lit)
            s = lit//i
            signs[i].add(s)
    for i in range(1,nAtoms):
        if len(signs[i]) == 1:   
            s, = signs[i]     
            if debug:
                print("Pure Literal", s*i)
            clauses, bindings = Propagate(clauses,bindings,i,s)
            return True, clauses, bindings
    return False, clauses, bindings


# make a deep copy of the clauses and the bindings, 
# so that destructive changes to one copy don't affect the other.

def CopyClauses(clauses,bindings):
    newClauses = []
    for c in clauses:
        newClauses += [c.copy()]
    return newClauses, bindings.copy()

# When there are no easy cases, and DPLL reaches a choice point,
# ChooseUnbound(clauses) implements a heuristic for choosing the atom
# to split on and the first sign to try with it, as follows:
# 1) Let maxL be the length of the shortest clause in clauses. 
#    E.g. if clauses contains clauses of length 2, 3, and 4, then maxL = 2.
# 2) Find the literal lit that occurs most often in clauses of length maxL 
#     (which have been collected in the list longestClauses).
#    E.g. if maxL = 2, and literal 2 occurs in 3 clauses of length 2, 
#          literal -3 occurs in 5, and literal -4 occurs in 1
#    then lit = -3
#    Return the atom and sign of lit, in this case 3 and -1
#    Note that if atom p occurs with sign s in k different clauses and maxL=2
#    then setting p to be s creates k different singleton clauses, which are all
#    easy cases. 
def ChooseUnbound(clauses):
    global nAtoms
    maxL = 0
    for c in clauses:
        if len(c) > maxL:
            maxL = len(c)
            longestClauses = [c]
        elif len(c) == maxL:
            longestClauses += [c]
    litCount = [0]*(2*nAtoms+1)
    max = 0
    for c in longestClauses:
        for lit in c:
            i = lit
            if i < 0:
                i = nAtoms-lit
            litCount[i] += 1
            if litCount[i] > max:
                imax = i
                max = litCount[i]
    if imax < nAtoms:
        return imax, 1
    else: 
        return imax-nAtoms, -1
        
# Assign the sign s to atom i in bindings, and propagate the effect to
# clauses. That is, delete any clause that contains s*i 
# and delete literal -s*i from any clause that contains it.

def Propagate(clauses,bindings,i,s):
    global debug
    if debug:
        print("Propagating atom", i, "sign", s)
    bindings[i]=s
    newClauses = clauses.copy()  # Note that this is a top level copy.
    for c in clauses:
        if s*i in c:
            newClauses.remove(c)
            if debug:
                print("Deleting clause", c)
        elif -s*i in c:
            if debug:
                print("Deleting literal ", -s*i, "from", c)
            c.remove(-s*i)
    return newClauses, bindings
     
        
# A few simple test examples

def test1():
    global debug
    debug = True
    clauses = [{1},{-1,2},{-1,-2,3}]
    return DPLLTop(clauses)

def test2():
    global debug
    debug = True
    clauses = [{1,2},{1,-2,-3},{2,3}]
    return DPLLTop(clauses)

def test3():
    global debug
    debug = True
    clauses = [{1, 2, 3}, {1, -2, -3}, {1, -4}, {-2, -3, -4}, {-1, -2, 3},
               {5, 6}, {5, -6}, {2, -5},{-3, -5}]
    return DPLLTop(clauses) 

def test4():
    global debug
    debug = True
    clauses = [{1,2},{1,-2},{-1,2},{-1,-2}]
    return DPLLTop(clauses) 

# Randomly generate a set of nClauses clauses all of length 3 with nAtoms different atoms
# seed is a seed for the random number generate. -1 if you don't want to set the seed.
# trace is a Boolean flag for verbose output.

def testRandom3SAT(nAtoms,nClauses,seed,trace):
   global debug
   if seed >= 0:
       np.random.seed(seed) 
   debug = trace
   clauses = []
   saveClauses = []
   for i in range(nClauses):
       atoms = np.random.choice(range(1,nAtoms+1),size=3,replace=False)
       signs = np.random.choice([1,-1],size=3,replace=True)
       clauses += [{int(atoms[0]*signs[0]), int(atoms[1]*signs[1]), int(atoms[2]*signs[2])}]
       saveClauses += [{int(atoms[0]*signs[0]), int(atoms[1]*signs[1]), int(atoms[2]*signs[2])}]
   if debug:
       print("Initial clauses:")
       for c in clauses:
           print(c)
       print("\n")       
   found, bindings = DPLLTop(clauses)
   if found:
       CheckAnswer(saveClauses,bindings)
   return found, bindings

def CheckAnswer(clauses,bindings):
    for c in clauses:
        ok = False
        for lit in c:
            if bindings[abs(lit)]*lit > 0:
                ok = True
        if not(ok):
            print("Wrong answer obtained!")
            print(clauses)
            print(bindings)
            return False
    return True  

# Try it with RandomTests(60,[230,240,260,280,300],100)

def RandomTests(nAtoms,clausesLengths,nTries):
    nlens = len(clausesLengths)
    counts = [0]*len(clausesLengths)
    for i in range(nlens):
        for j in range(nTries):
            found, bindings = testRandom3SAT(nAtoms, clausesLengths[i],-1,False)
            if found:
                counts[i] += 1
        print("With", nAtoms, "atoms and", clausesLengths[i], "clauses,", 
               "the fraction satisfiable is", counts[i]/nTries)
    return counts 
import sys
def input_file(filename):
  lines=[]
  with open(filename) as ip:
    for line in ip:
      if line:
        lines.append(line)
  fst_line = lines[0].split()

  total_V = int(fst_line[0])
  #print(total_V)
  empty_V = int(fst_line[1])
  #print(empty_V)
  Z = int(fst_line[2])
  #print(Z)
  Init_state = lines[1].split()
  #print(Init_state)
  Goal_state = lines[2].split()
  #print(Goal_state)
  connected=[]
  for i in range(0,total_V+1):
    v=set()
    connected.append(v)
  for i in range(3, len(lines)):
    #print(lines[i])
    cur_line = lines[i].split()
    fst_num =int(cur_line[0])
    sec_num =int(cur_line[1])
    connected[fst_num].add(sec_num)
    connected[sec_num].add(fst_num)
  #print(connected)
  return total_V, empty_V, Z, Init_state, Goal_state, connected

def literal_generation(total_V, empty_V, Z, connected):
  upper_list = [chr(i) for i in range(65, 91)]
  letter_num = total_V-empty_V
  #print(upper_list[0])
  literal_map={}
  num_flag=1
  #In(P,V,T), eg. In(A,5,3)
  IN_P_V_T = []
  NEG_IN_P_V_T = []
  for i in range(0, letter_num):
    each_letter=[]
    neg_each_letter=[]
    IN_P_V_T.append(each_letter)
    NEG_IN_P_V_T.append(neg_each_letter)
    for j in range(0, total_V+1):
      each_vertex=[]
      neg_each_vertex=[]
      IN_P_V_T[i].append(each_vertex)
      NEG_IN_P_V_T[i].append(neg_each_vertex)
      for k in range(0, Z+1):
        elem="In("+upper_list[i]+","+str(j)+","+str(k)+")"
        neg_elem="~In("+upper_list[i]+","+str(j)+","+str(k)+")"
        literal_map[elem]=num_flag
        literal_map[neg_elem]=-num_flag
        num_flag+=1
        IN_P_V_T[i][j].append(elem)
        NEG_IN_P_V_T[i][j].append(neg_elem)
  #IN_P_V_T[letters(0,letter_num-1)][vertex(1,totalV)][move(0,Z+1)]

  #print(literal_map["-In(A,2,0)"])
  #Empty(V,T)
  EMPTY_V_T = []
  NEG_EMPTY_V_T = []
  for i in range(0, total_V+1):
    each_vertex=[]
    neg_each_vertex=[]
    EMPTY_V_T.append(each_vertex)
    NEG_EMPTY_V_T.append(neg_each_vertex)
    for j in range(0, Z+1):
      #EMPTY_V_T[i].append("666")
      elem="Empty("+str(i)+","+str(j)+")"
      neg_elem="~Empty("+str(i)+","+str(j)+")"
      literal_map[elem]=num_flag
      literal_map[neg_elem]=-num_flag
      num_flag+=1
      EMPTY_V_T[i].append(elem)
      NEG_EMPTY_V_T[i].append(neg_elem)
  #EMPTY_V_T[vertext(1,totalV)][move(0,Z+1)]

  #Move(U,V,T)
  MOVE_U_V_T = []
  NEG_MOVE_U_V_T = []
  for i in range(0, total_V+1):
    each_U=[]
    neg_each_U=[]
    MOVE_U_V_T.append(each_U)
    NEG_MOVE_U_V_T.append(neg_each_U)
    for j in range(0, total_V+1):
      each_V=[]
      neg_each_V=[]
      MOVE_U_V_T[i].append(each_V)
      NEG_MOVE_U_V_T[i].append(neg_each_V)
      for k in range(0, Z+1):
        if(i!=j):
          elem="Move("+str(i)+","+str(j)+","+str(k)+")"
          neg_elem="~Move("+str(i)+","+str(j)+","+str(k)+")"
          literal_map[elem]=num_flag
          literal_map[neg_elem]=-num_flag
          num_flag+=1
          MOVE_U_V_T[i][j].append(elem)
          NEG_MOVE_U_V_T[i][j].append(neg_elem)
  #MOVE_U_V_T[vertex(1,totalV)][vertex(1,totalV)][move(0,Z+1)]
  #print(literal_map["In(A,1,0)"])
  return IN_P_V_T, EMPTY_V_T, MOVE_U_V_T, literal_map

def clause_generation(IN_P_V_T, EMPTY_V_T, MOVE_U_V_T, total_V, empty_V, Z, connected, Init_state, Goal_state, literal_map):
  clause_list=[]
  letter_num = total_V-empty_V
  #form1 empty(V,T) <=> -In(P1,V,T) v -In(P2,V,T) v -In(p3, V, T)
  for i in range(0,Z+1):
    for j in range(1, total_V+1):
      elem_set=set()
      for k in range(0, letter_num):
        neg_elem_set=set()
        print("~"+EMPTY_V_T[j][i]+" V "+"~"+IN_P_V_T[k][j][i])
        neg_elem_set.add("~"+EMPTY_V_T[j][i])
        neg_elem_set.add("~"+IN_P_V_T[k][j][i])
        clause_list.append(neg_elem_set)
      cur_str=EMPTY_V_T[j][i]
      elem_set.add(cur_str)
      for z in range(0, letter_num):
        cur_in = IN_P_V_T[z][j][i]
        cur_str+=" V "+cur_in
        elem_set.add(cur_in)
      print(cur_str)
      clause_list.append(elem_set)
  #print(len(form1_list))
  print("\n")    

  #form2 ¬[In(P,V,0) ∧ In(Q,V,0)] and ¬[In(P,V,Z) ∧ In(Q,V,Z)]
  for i in range(0, letter_num):
    for j in range(i+1, letter_num):
      for k in range(1, total_V+1):
        neg_elem_set=set()
        print("~"+ IN_P_V_T[i][k][0]+"V ~", IN_P_V_T[j][k][0])
        neg_elem_set.add("~"+ IN_P_V_T[i][k][0])
        neg_elem_set.add("~"+ IN_P_V_T[j][k][0])
        clause_list.append(neg_elem_set)
  for i in range(0, letter_num):
    for j in range(i+1, letter_num):
      for k in range(1, total_V+1):
        neg_elem_set=set()
        print("~"+ IN_P_V_T[i][k][Z]+"V ~", IN_P_V_T[j][k][Z])
        neg_elem_set.add("~"+ IN_P_V_T[i][k][Z])
        neg_elem_set.add("~"+ IN_P_V_T[j][k][Z])
        clause_list.append(neg_elem_set)
  print("\n")

  #form3 For each pair adjacent squares U and V and time T from 0 to Z-1, the following is an axiom
  #If, at time T you move piece P from U to V, then at time T, U s not empty and V is empty.
  for i in range(0, Z):
    for j in range(1, len(connected)):
      for k in connected[j]:
        elem_set1=set()
        elem_set2=set()
        #print(k)
        neg_move1="~Move("+str(j)+","+str(k)+","+str(i)+")"
        elem_set1.add(neg_move1)
        #print(neg_move1)
        neg_empty="~Empty("+str(j)+","+str(i)+")"
        elem_set1.add(neg_empty)
        print(neg_move1+" V "+neg_empty)
        neg_move2="~Move("+str(j)+","+str(k)+","+str(i)+")"
        elem_set2.add(neg_move2)
        empty="Empty("+str(k)+","+str(i)+")"
        elem_set2.add(empty)
        print(neg_move2+" V "+empty)
        clause_list.append(elem_set1)
        clause_list.append(elem_set2)
  print("\n")

  #form4 For each piece P, connected vertices U and V and time T between 0 and Z-1, the folowing is an axiom
  #If, at time T piece P is in U and you move it to V then at time T+1, P is in V.
  upper_list = [chr(i) for i in range(65, 91)]
  for i in range(0, Z):
    for j in range(1, len(connected)):
      for k in connected[j]:
        for l in range(0,letter_num):
          elem_set=set()
          neg_in="~In("+upper_list[l]+","+str(j)+","+str(i)+")"
          elem_set.add(neg_in)
          neg_move="~Move("+str(j)+","+str(k)+","+str(i)+")"
          elem_set.add(neg_move)
          In="In("+upper_list[l]+","+str(k)+","+str(i+1)+")"
          elem_set.add(In)
          print(neg_in+" V "+neg_move+" V "+In)
          clause_list.append(elem_set)
  print("\n")    

  #form5 For any pair of connected vertices U and V and time T between 0 and Z-1, the folowing is an axiom
  #If, at time T you move a piece from U to V, then at time T+1, U is empty.
  for i in range(0, Z):
    for j in range(0, len(connected)):
      for k in connected[j]:
        elem_set=set()
        neg_move="~Move("+str(j)+","+str(k)+","+str(i)+")"
        elem_set.add(neg_move)
        empty="Empty("+str(j)+","+str(i+1)+")"
        elem_set.add(empty)
        print(neg_move+" V "+empty)
        clause_list.append(elem_set)
  print("\n")

  #form6 For vertex V, and time T between 0 and Z-1, if V is empty at T but not at time T+1
  #then at time T some piece is moved from neighboring square U into V
  for i in range(0, Z):
    for j in range(1, len(connected)):
      elem_set=set()
      neg_empty="~Empty("+str(j)+","+str(i)+")"
      elem_set.add(neg_empty)
      empty="Empty("+str(j)+","+str(i+1)+")"
      elem_set.add(empty)
      cur_str=""
      for k in connected[j]:
        cur_str+=" V "+"Move("+str(k)+","+str(j)+","+str(i)+")"
        elem_set.add("Move("+str(k)+","+str(j)+","+str(i)+")")
      print(neg_empty+" V "+empty+cur_str)
      clause_list.append(elem_set)
  print("\n")  

  #form7 For vertex V, and time T between 0 and Z-1, if V is not empty at T but is empty at time T+1
  #then at time T some piece is moved from V into neighboring square U.
  for i in range(0, Z):
    for j in range(1, len(connected)):
      elem_set=set()
      neg_empty="Empty("+str(j)+","+str(i)+")"
      elem_set.add(neg_empty)
      empty="~Empty("+str(j)+","+str(i+1)+")"
      elem_set.add(empty)
      cur_str=""
      for k in connected[j]:
        cur_str+=" V "+"Move("+str(j)+","+str(k)+","+str(i)+")"
        elem_set.add("Move("+str(j)+","+str(k)+","+str(i)+")")
      print(neg_empty+" V "+empty+cur_str)
      clause_list.append(elem_set)
  #print(form7_list)
  print("\n")

  #form 8 If piece P is at vertex V at time T, then at time T+1, either P is still at V or V is empty.
  for i in range(0,Z):
    for j in range(1, total_V+1):
      for k in range(0, letter_num):
        elem_set=set()
        neg_in1="~In("+upper_list[k]+","+str(j)+","+str(i)+")" 
        neg_in2="In("+upper_list[k]+","+str(j)+","+str(i+1)+")" 
        empty="Empty("+str(j)+","+str(i+1)+")"
        elem_set.add(neg_in1)
        elem_set.add(neg_in2)
        elem_set.add(empty)
        print(neg_in1+" V "+neg_in2+" V "+empty)
        clause_list.append(elem_set)
  print("\n")

  #form 9 For any two distinct edges U-V and W-X (the two edges can have one vertex in common, but not both) 
  #and any time T between 0 and Z-1,¬[Move(U,V,T) ∧ Move(W,X,T)] is an axiom
  for i in range(0,Z):
    for j in range(1, len(connected)):
      cur_lst=[]
      for k in connected[j]:
        cur_lst.append(k)
      for k in range(0, len(cur_lst)):
        for l in range(k+1,len(cur_lst)):
          elem_set=set()
          neg_move1="~Move("+str(j)+","+str(cur_lst[k])+","+str(i)+")"
          neg_move2="~Move("+str(j)+","+str(cur_lst[l])+","+str(i)+")"
          elem_set.add(neg_move1)
          elem_set.add(neg_move2)
          print(neg_move1+" V "+neg_move2)
          clause_list.append(elem_set)
      for k in connected[j]:
        for l in range(j+1, len(connected)):
          for m in connected[l]:
            elem_set=set()
            neg_move1="~Move("+str(j)+","+str(k)+","+str(i)+")"
            neg_move2="~Move("+str(l)+","+str(m)+","+str(i)+")"
            elem_set.add(neg_move1)
            elem_set.add(neg_move2)
            print(neg_move1+" V "+neg_move2)
            clause_list.append(elem_set)
  print("\n")
  #form 10 For each vertex V either specify the piece in V at time 0 or specify that it is empty at time 0.
  for i in range(0, len(Init_state)):
    #print(Init_state[i])
    if Init_state[i]!="Empty":
      for j in range(0, letter_num):
        if(Init_state[i]==IN_P_V_T[j][i+1][0][3:4]):
          elem_set=set()
          elem_set.add(IN_P_V_T[j][i+1][0])
          print(IN_P_V_T[j][i+1][0])
          clause_list.append(elem_set)
    else:
      elem_set=set()
      elem_set.add(EMPTY_V_T[i+1][0])
      print(EMPTY_V_T[i+1][0])
      clause_list.append(elem_set)
  print("\n")

  #form 11 For each vertex V either specify the piece in V at time Z or specify that it is empty at time Z.
  for i in range(0, len(Goal_state)):
    #print(Init_state[i])
    if Goal_state[i]!="Empty":
      for j in range(0, letter_num):
        if(Goal_state[i]==IN_P_V_T[j][i+1][Z][3:4]):
          elem_set=set()
          elem_set.add(IN_P_V_T[j][i+1][Z])
          print(IN_P_V_T[j][i+1][Z])
          clause_list.append(elem_set)
    else:
      elem_set=set()
      elem_set.add(EMPTY_V_T[i+1][Z])
      print(EMPTY_V_T[i+1][Z])
      clause_list.append(elem_set)
  #print(form11_list)
  print("\n")
  num_lst=[]
  for i in range(0, len(clause_list)):
    num_set=set()
    for j in clause_list[i]:
      num_set.add(literal_map[j])
    num_lst.append(num_set)
  return num_lst
def main():
    if len(sys.argv)!=2:
        print("wrong parameter numbers")
        sys.exit(1)
    input_file_name = sys.argv[1]
    total_V, empty_V, Z, Init_state, Goal_state, connected=input_file(input_file_name)
    IN_P_V_T, EMPTY_V_T, MOVE_U_V_T, literal_map = literal_generation(total_V, empty_V, Z, connected)
    lst=clause_generation(IN_P_V_T, EMPTY_V_T, MOVE_U_V_T, total_V, empty_V, Z, connected, Init_state, Goal_state, literal_map)
    #test3()
    found, bindings =DPLLTop(lst)
    for i in range(0, len(bindings)):
        for j in literal_map:
            if(i==literal_map[j] and j[0:4]=="Move" and bindings[i]==1):
                print(j)
if __name__ == '__main__':
  main()
