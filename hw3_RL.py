import sys
import random
import numpy as np
def input_file(file_name):
  lines = []
  with open(file_name) as ip:
    for line in ip:
      if line:
        lines.append(line)

  fst_line=lines[0].split()
  non_terminal_num=int(fst_line[0])
  terminal_num=int(fst_line[1])
  action_num=int(fst_line[2])
  round_num=int(fst_line[3])
  freq_num=int(fst_line[4])
  M=int(fst_line[5])
  total_state=non_terminal_num+terminal_num
  #print(non_terminal_num,terminal_num,action_num,round_num,freq_num,M)
  #print("\n")
  terminal_reward_map={}
  sec_line=lines[1].split()
  for i in range(0,len(sec_line),2):
    ter_state=int(sec_line[i])
    terminal_reward=int(sec_line[i+1])
    #print(ter_state, terminal_reward)
    terminal_reward_map[ter_state]=terminal_reward
  #print("\n")
  third_line=list(map(float,lines[2].split()))
  act_cost={}
  for i in range(0,len(third_line), 2):
    action=int(third_line[i])
    cost= third_line[i+1]
    #print(action, cost)
    act_cost[action]=cost

  starting_state=np.zeros((total_state,total_state,action_num))
  #starting_state=[total_state][total_state][action_num]
  for i in range(3,len(lines)):
    line=lines[i].split()
    start=int(line[0][0:1])
    action=int(line[0][2:3])
    #print(start, action)
    for j in range(1,len(line),2):
      end=int(line[j])
      prob=float(line[j+1])
      #print(start,end,action,prob)
      starting_state[start][end][action]=prob
  #print(starting_state)

  return non_terminal_num,terminal_num,total_state,action_num,round_num,freq_num,M,terminal_reward_map,act_cost,starting_state

def chooseAction(state,count, total, M, action_num, terminal_reward_map):
   for i in range(action_num):
     if count[state][i]==0:
       return i
   avg=[]
   for i in range(action_num):
    avg.append(total[state][i]/count[state][i])
   bottom = min(np.min(avg),min(terminal_reward_map.values()))
   up = max(terminal_reward_map.values())
   scaled_avg =[]
   for i in range(action_num): scaled_avg.append(0.25+0.75*(avg[i]-bottom)/(up-bottom))
   c = sum(count[state])
   up=[]
   for i in range(action_num): up.append(scaled_avg[i]**(c/M))
   norm=sum(up)
   p=[]
   for i in range(action_num): p.append(up[i]/norm)
   return random.choices(range(action_num),p)[0]

def output (count, total, cur_round):
   print("After "+str(cur_round)+" rounds")
   print("Count: ")
   for i in range(len(count)):
     rst=""
     for j in range(len(count[i])):
       rst+="["+str(i)+"]["+str(j)+"]="+str(count[i][j])+". "
     print(rst)
   print("Total: ")
   for i in range(len(total)):
     rst=""
     for j in range(len(total[i])):
      r = round(total[i][j], 1)
      rst+="["+str(i)+"]["+str(j)+"]="+str(r)+". "
     print(rst)

   rst = "Best Action: "
   for i in range(len(total)):
     All_zero = True
     max_avg=-float('inf')
     best_action=-1
     for j in range(len(total[i])):
       if count[i][j]>0:
         All_zero = False
         current_avg = total[i][j]/count[i][j]
         if current_avg>max_avg:
          max_avg=current_avg
          best_action=j
     if All_zero:
       rst+=str(i)+": U. "
     else:
       rst+=str(i)+": "+str(best_action)+" "
   print(rst)

def running(non_terminal_num,terminal_num,total_state,action_num,round_num,freq_num,M,terminal_reward_map,act_cost,starting_state):
   count = [[0 for _ in range(action_num)] for _ in range(non_terminal_num)]
   total = [[0.0 for _ in range(action_num)] for _ in range(non_terminal_num)]
   #print("Round num:"+str(round_num))
   for i in range(round_num):
     current_state = random.choices(range(non_terminal_num))[0]
     total_cost=0
     visited = []
     while True:
      if current_state in terminal_reward_map:
         reward = terminal_reward_map[current_state]
         net_reward = reward - total_cost
         break

      chosen_action = chooseAction(current_state, count, total, M, action_num, terminal_reward_map)
      total_cost += act_cost[chosen_action]

      cur_pair = (current_state, chosen_action)
      #if cur_pair not in visited:
      visited.append(cur_pair)
      next_state_prob = starting_state[current_state,:,chosen_action]
      #?
      current_state = random.choices(range(total_state), next_state_prob)[0]

     for pair in visited:
        count[pair[0]][pair[1]] += 1
        total[pair[0]][pair[1]] += net_reward

     #print(i)
     if freq_num > 0 and (i+1)%freq_num ==0: output(count, total, i+1)
     elif freq_num == 0: output(count, total, i+1)
     elif i+1==round_num:
      #print("here3!!")
      output(count, total, i+1)


def main():
    if len(sys.argv)!=2:
        print("wrong parameter numbers")
        sys.exit(1)
    input_file_name = sys.argv[1]
    non_terminal_num,terminal_num,total_state,action_num,round_num,req_num,M,terminal_reward_map,act_cost,starting_state=input_file(input_file_name)
    running(non_terminal_num,terminal_num,total_state,action_num,round_num,req_num,M,terminal_reward_map,act_cost,starting_state)

main()
