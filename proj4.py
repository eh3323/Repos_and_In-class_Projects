from itertools import count
import math
import re
import sys
def input_file(file_name, N):
  lines = []
  count=0
  category_count =False
  category_num =set()
  category_numWithName={}
  jump_flag = False
  with open(file_name) as ip:
    for line in ip:
      if not line.strip():
        jump_flag = True
        if count == N:
          break
      if (line.strip() and jump_flag) or count==0:
        lines.append(line.strip())
        count +=1
        jump_flag = False
        next_line = next(ip, None)
        lines.append(next_line.strip())
        next_line = next_line.strip().lower()
        category_numWithName[line.strip().lower()] = next_line
        category_num.add(next_line)
      elif line.strip() and not jump_flag:
        lines.append(line.strip())
  return lines, category_num, category_numWithName

def combinestring(list):
  rst=''
  for i in range(len(list)):
    if(i!=len(list)-1):
      rst+=list[i]+' '
    else:
      rst+=list[i]
  return rst

def input_processing(words_file, lines, name):

  name_set=set()
  for i in name:
    name_set.add(i)

  temp_words = []
  with open(words_file) as wf:
    for word in wf:
      temp_words.append(word.strip())
  words=set()
  for i in range(len(temp_words)):
    temp=temp_words[i].split()
    for j in range(len(temp)):
      words.add(temp[j])
#lower case all words
  for i in range(len(lines)):
    lines[i] = lines[i].split()
  for i in range(len(lines)):
    for j in range(len(lines[i])):
      lines[i][j]=lines[i][j].lower() 
#remove all words that is in the given list
  for i in range(len(lines)):
    new_line=[]
    #print(cur_set)
    for j in range(len(lines[i])):
      if lines[i][j] not in words:
        new_line.append(lines[i][j])
    lines[i] = new_line
#remove all words that has only 1-2letters
  for i in range(len(lines)):
    new_line=[]
    for j in range(len(lines[i])):
      the_name=combinestring(lines[i])
      if len(lines[i][j])>=3 or the_name in name_set:
        new_line.append(lines[i][j])
    lines[i] = new_line
#remove repetitive words  
  fst_pos=0
  end_pos=1
  while True:
    temp_name=combinestring(lines[end_pos])
    if temp_name in name_set:
      corpus=set()
      for i in range(fst_pos+2,end_pos):
        new_line=[]
        for j in range(len(lines[i])):
          if lines[i][j] not in corpus:
            new_line.append(lines[i][j])
            corpus.add(lines[i][j])
        lines[i]= new_line
      fst_pos=end_pos
      end_pos+=1
    elif end_pos==len(lines)-1:
      for i in range(fst_pos+2,end_pos):
        new_line=[]
        for j in range(len(lines[i])):
          if lines[i][j] not in corpus:
            new_line.append(lines[i][j])
            corpus.add(lines[i][j])
        lines[i]= new_line
      break
    else:
      end_pos+=1
  #print(lines)
  for i in range(len(lines)):
    for j in range(len(lines[i])):
      cur= re.split(r'[.,\s]+', lines[i][j])
      lines[i][j]=combinestring(cur)
      lines[i][j]=lines[i][j].strip()
  return lines

def counting(lines, category_num, name):
  category_count={}
  word_category_count={}
  for i in category_num:
    category_count[i] = 0
  for i in range(len(lines)):
    for j in range(len(lines[i])):
      if lines[i][j] in category_num:
        temp_name=combinestring(lines[i-1])
        if temp_name in name and name[temp_name] == lines[i][j]:
          category_count[lines[i][j]] += 1
  fst_pos=1
  end_pos=2
  repetitive_set=set()
  while True:
    temp_name = combinestring(lines[end_pos-1])
    if temp_name in name and lines[end_pos][0] in category_num  and name[temp_name] == lines[end_pos][0]:
      for i in range(fst_pos+1, end_pos-1):
        for j in range(len(lines[i])):
          cur_list = (lines[fst_pos][0], lines[i][j])
          if cur_list not in word_category_count:
            #print(cur_list)
            word_category_count[cur_list] = 1  
            #name_flag=temp_name     
          elif cur_list in word_category_count:
            #print(cur_list)
            repetitive_set.add(cur_list)
            word_category_count[cur_list] += 1
            #name_flag = temp_name
      fst_pos = end_pos
      end_pos +=1
    elif end_pos == len(lines)-1:
      end_pos+=1
      for i in range(fst_pos+1, end_pos):
        for j in range(len(lines[i])):
          cur_list = (lines[fst_pos][0], lines[i][j])
          if cur_list not in word_category_count:
            #print(cur_list)
            word_category_count[cur_list] = 1
          elif cur_list in word_category_count:
            #print(cur_list)
            repetitive_set.add(cur_list)
            word_category_count[cur_list] += 1
            #name_flag = temp_name
      break
    else:
      end_pos +=1 

#add up words with irrelevant categories
  rest_pairs={}
  for elem in category_num:
    for elem2 in word_category_count:
      if elem != elem2[0]:
        cur_list = (elem, elem2[1])
        if cur_list not in word_category_count:
          rest_pairs[cur_list] = 0


  word_category_count.update(rest_pairs)
  #for elem in word_category_count:
  #print(elem)
  #print(category_count)
  #print(word_category_count)
  return category_count, word_category_count

def probability(num_category, count_word_category):
  Freq_C={}
  Freq_WC={}
  total_C= sum(num_category.values())
  for elem in num_category:
    Freq_C[elem] = num_category[elem]/total_C
  for elem in count_word_category:
    Freq_WC[elem] = count_word_category[elem]/num_category[elem[0]]
  P_C={}
  P_WC={}
  param=0.1
  for elem in Freq_C:
    P_C[elem] = (Freq_C[elem]+param)/(1+len(num_category)*param)
  for elem in Freq_WC:
    P_WC[elem] = (Freq_WC[elem]+param)/(1+2*param)
  L_C={k:-1* math.log2(v) for k,v in P_C.items()}
  L_WC={k:-1 * math.log2(v) for k,v in P_WC.items()}
  return L_C, L_WC

def test_input_file(file_name, N):
  empty_flag=0
  test_lines=[]
  category_num = set()
  category_numWithName = {}
  jump_flag=False
  with open(file_name) as ip:
    for line in ip:
      if empty_flag==0:
        empty_flag+=1
        continue
      elif line.strip() and not jump_flag and empty_flag<N:
        continue
      elif not line.strip() and empty_flag<N:
        jump_flag=True
      elif jump_flag and line.strip() and empty_flag<N:
        empty_flag+=1
        jump_flag=False
      #不空行，但上一行是空行，是test set
      elif line.strip() and empty_flag>=N and jump_flag:
        test_lines.append(line.strip())
        jump_flag=False
        next_line = next(ip, None)
        test_lines.append(next_line.strip())
        next_line = next_line.strip().lower()
        category_numWithName[line.strip().lower()] = next_line
        category_num.add(next_line)
        empty_flag+=1
      #不空行，但上一行不是空行，是test set
      elif line.strip() and empty_flag>N and not jump_flag:
        test_lines.append(line.strip())
      elif not line.strip() and empty_flag>=N:
        jump_flag=True
  return test_lines, category_num, category_numWithName

def test(words_file_name,file_name, N, L_C, L_PC, num_category, count_word_category, name):
  test_lines, category_num, category_numWithName = test_input_file(file_name, N)
  test_lines = input_processing(words_file_name, test_lines, category_numWithName)
  fst_pos=1
  end_pos=2
  test_category={}
  num_correct=0
  num_total=0
  while True:
    temp_name = combinestring(test_lines[end_pos-1])
    if temp_name in category_numWithName and test_lines[end_pos][0] in category_num and category_numWithName[temp_name] == test_lines[end_pos][0]:     
      test_category=L_C.copy()
      for i in range(fst_pos+1, end_pos-1):
        for j in range(len(test_lines[i])):
          for elem in category_num:
            cur_list = (elem, test_lines[i][j])    
            if cur_list in L_PC:
              test_category[elem]+=L_PC[cur_list]
      min=1000
      rst=''
      ans=''
      for elem in test_category:
        if test_category[elem]<min:
            min=test_category[elem]
            rst=elem
      if rst== test_lines[fst_pos][0]:
        ans="Correct"
        num_correct+=1
        num_total+=1
      else:
        ans="Wrong"
        num_total+=1
      print(combinestring(test_lines[fst_pos-1]), "prediction:", rst,"." , ans)
      
      m = 1000
      for i in test_category:
        if test_category[i]<m:
          m=test_category[i]
      X=test_category.copy()
      for elem in test_category:
        if test_category[elem]-m<7:
          X[elem]=2**(m-test_category[elem])
        else:
          X[elem]=0
      total=sum(X.values())
      for elem in X:
        X[elem]=X[elem]/total
      for elem in X:
        print(elem, ":", round(X[elem],2))
      fst_pos = end_pos
      end_pos +=1
    
    elif end_pos == len(test_lines)-1:
      end_pos+=1
      test_category=L_C.copy()
      for i in range(fst_pos+1, end_pos):
        for j in range(len(test_lines[i])):
          for elem in category_num:
            cur_list = (elem, test_lines[i][j])
            if cur_list in L_PC:
              test_category[elem]+=L_PC[cur_list]
      min=1000
      rst=''
      ans=''
      for elem in test_category:
        if test_category[elem]<min:
            min=test_category[elem]
            rst=elem
      if rst== test_lines[fst_pos][0]:
        ans="Correct"
        num_correct+=1
        num_total+=1
      else:
        ans="Wrong"
        num_total+=1
      print(combinestring(test_lines[fst_pos-1]), "prediction:", rst,"." , ans)
      m = 1000
      for i in test_category:
        if test_category[i]<m:
          m=test_category[i]
      X=test_category.copy()
      for elem in test_category:
        if test_category[elem]-m<7:
          X[elem]=2**(m-test_category[elem])
        else:
          X[elem]=0
      total=sum(X.values())
      for elem in X:
        X[elem]=X[elem]/total
      for elem in X:
        print(elem, ":", round(X[elem],2))
      break
    else:
      end_pos +=1 
  print("Overall Accuracy:",num_correct,"out of",num_total, "=", round(num_correct/num_total,2))
  return

def main():
    if len(sys.argv)!=3:
        print("wrong parameter numbers")
        sys.exit(1)
    input_file_name = sys.argv[1]
    NN=int(sys.argv[2])
    lines, category_num, name=input_file(input_file_name, NN)
    words_file_name = 'words.txt'
    lines = input_processing(words_file_name, lines, name)
    Num_Category, Count_Word_Category = counting(lines, category_num, name)
    C, WC=probability(Num_Category, Count_Word_Category)
    rst=test(words_file_name, input_file_name, NN, C, WC, Num_Category, Count_Word_Category, name)
if __name__ == '__main__':
  main()
