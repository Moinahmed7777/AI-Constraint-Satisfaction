# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:02:20 2020

@author: Necro

"""
"""
Constraint Satisfaction problem
Forward Checking not implemented, Need to make it more efficient, many redundant code in picking var and scanning cons, needs better.
Object-Oriented approach
"""
import operator
from heapq import heappush, heappop
import copy


    
class Node: 
      
    def __init__(self, data): 
        self.data = data 
        self.next = None
class Stack: 
      
    # head is default NULL 
    def __init__(self): 
        self.head = None
    # Checks if stack is empty 
    def isempty(self): 
        if self.head == None: 
            return True
        else: 
            return False
      
    # Method to add data to the stack 
    # adds to the start of the stack 
    def push(self,data): 
          
        if self.head == None: 
            self.head=Node(data)
              
        else: 
            newnode = Node(data)
            newnode.next = self.head 
            self.head = newnode 
      
    # Remove element that is the current head (start of the stack) 
    def pop(self): 
          
        if self.isempty(): 
            return None
              
        else: 
            # Removes the head node and makes  
            #the preceeding one the new head 
            
            poppednode = self.head 
            self.head = self.head.next
            poppednode.next = None
            return poppednode.data 
      
    # Returns the head node data 
    def peek(self): 
          
        if self.isempty(): 
            return None
              
        else: 
            return self.head.data 



def test_goal(state):
    TC=0
    FC=0
    NC=0
    g=len(state.config_cons)
    l=[[None] for i in range(g)]
    X=None
    Y=None
    for i in range(len(state.config_cons)):
        if state.config_cons[i][0] in state.dictA and state.config_cons[i][2] in state.dictA :
            X=state.dictA[state.config_cons[i][0]]
            Y=state.dictA[state.config_cons[i][2]]
            
        else:
            
            continue
        
        if X ==None or Y==None:
            continue
        if state.op[state.config_cons[i][1]](X,Y):
            l[i]=True
            
        else:
            l[i]=False
        
    
    for i in l:
        if i == True:
            TC+=1
        if i==False:
            FC+=1
        if i==None:
            NC+=1
    return (TC,FC,NC)
    

def printf(X):
    s=''
    lenans=len(X)
    
    for i in range(len(X)):
        D=" "+X[i][0]+'='+str(X[i][1])
        if i !=lenans-1:
            D+=","
        s+=D
    return s
    
def dfs_search(initial_state):

    
    s= Stack()
    s.push(initial_state)
    count = 0
    c=0
    while not s.isempty():
        
        state=s.head.data
        s.pop()
        TC,FC,NC=test_goal(state)
        
        if FC>0:
            ans=printf(state.assign)
            c+=1
            print(str(c)+"."+ans + " failure")
            continue
        if TC==len(state.config_cons):
            ans=printf(state.assign)
            c+=1
            print(str(c)+"."+ans + " solution")
            
            break
           
        
        count=count+1
        
        for neighbor in state.ex()[::-1]:
            s.push(neighbor)
            
class PuzzleState(object):


    def __init__(self, assign,config_vars,config_cons,parent=None,depth=0,dictA={}):


        self.config_vars = config_vars
        self.config_cons = config_cons
        
        
        self.parent = parent
        self.assign=assign
        self.dictA=dictA
        self.depth=depth
        self.children=[]
        self.op={"<":operator.lt,
                 ">":operator.gt,
                 "!":operator.ne,
                 "=":operator.eq,
                }
        
    def p_var(self,as_vars):
        H=[]
        for key,val in self.config_vars.items():
            if len(as_vars)==0:
                H.append((len(val),key))
            else:
                as_tup=self.assign_tup()
                if key in as_tup:
                    continue
                else:
                    H.append((len(val),key))
                    
            
        H.sort()
        heap1=[]
        while not len(H)==0:
            num,state=H.pop(0)
            
            count=0
            for j in self.config_cons:
                if state in j:
                    if self.test3(j):
                        continue
                    else:
                        count+=1
            
            heappush(heap1,(num,-count,state))    
            
        if len(heap1)==0:
            return None
        else:
            return heappop(heap1)[2]
        
    def test3(self,j):
        for i in self.assign_tup():
            if i in j:
                return True
        return False
        
    
    def assign_tup(self):
        as_tup=[]
        for i in self.assign:
            #print("i",i)
            as_tup.append(i[0])
        return tuple(as_tup)
   
    def test(self,v1,val1,v2,val2):
        for i in self.config_cons:
            if v1 in i and v2 in i:
                if i[0]==v1:
                    X=val1
                    Y=val2
                else:
                    X=val2
                    Y=val1
                
                if self.op[i[1]](X,Y):
                    return 1
                else:
                    return 0
       
                
                
    def LCV(self,variable,value):
        TC=0
        for k,v in self.config_vars.items():
            if k in self.assign_tup() or variable==k:
                continue
            for i in v:
                if self.test(variable,value,k,i)==None:
                    continue
                TC+=self.test(variable,value,k,i)
        
        return -(TC)                
    
    
        
    def ex(self):
        variable=self.p_var(self.assign)
        if variable==None:
            return self.children
        get_var_val=self.config_vars.get(variable)
        
        
        heap=[]
        for value in get_var_val:
            heappush(heap,(self.LCV(variable,value),value))
        
        while not len(heap)==0:
            X=heappop(heap)[1]
            
            Xlist=copy.deepcopy(self.assign)
            Xdict=copy.deepcopy(self.dictA)
            Xdict[variable]=X
            As_tup=(variable,X)
            Xlist.append(As_tup)
            self.children.append(PuzzleState(Xlist,self.config_vars,self.config_cons,parent=self,depth=self.depth+1,dictA=Xdict))
        
        return self.children
        


def main():
    #Var_dictx contains a dictionary of Variables
    #Cons_listx contains a list of Contraints
    
    #Test Case 1:
    Var_dict1={"A": [1, 2, 3],
               "B": [1, 2, 3],
               "C": [1, 3, 4]}
    
    Cons_list1=[("A", "<", "B"),
                ("A",">","C"),
                ("B",">","C")]

    #Test Case 2:
    Var_dict2={"A": [1, 2, 3,4,5],
               "B": [1, 2, 3,4,5],
               "C": [1, 2, 3,4,5],
               "D": [1, 2, 3,4,5],
               "E": [1,2,3],
               "F": [1,2]}

    Cons_list2=[('A', '>', 'B'),
                ('B', '>', 'F'),
                ('A', '>', 'C'),
                ('C', '>', 'E'),
                ('A', '>', 'D'),
                ('D', '=' ,'E')]
    
    #Test Case 3:
    Var_dict3={"A": [1, 2, 3,4,5],
               "B": [1, 2, 3,4],
               "C": [1, 2, 3,4,5,6,7,8],
               "D": [5,7,9,11],
               "E": [3,4,5,6],
               "F": [1,5,10],
               "G": [5,6,7,8,9]}
    
    Cons_list3=[('A', '=' ,'G'),
                ('A', '>', 'B'),
                ('C', '>', 'B'),
                ('D', '>', 'E'),
                ('G', '>', 'C')]
    
   
    Initial_state1=PuzzleState([],Var_dict1,Cons_list1)
    Initial_state2=PuzzleState([],Var_dict2,Cons_list2)
    Initial_state3=PuzzleState([],Var_dict3,Cons_list3)
    print("Constraint Satisfaction problem ")
    print("No consistency-enforcing procedure is applied\n")
    
    print("Solutions for Test Case 1 :\n")
    dfs_search(Initial_state1)
    print('\n')
    print("Solutions for Test Case 2 :\n")
    dfs_search(Initial_state2)
    print('\n')
    print("Solutions for Test Case 3 :\n")
    dfs_search(Initial_state3)
        
    
if __name__ == '__main__':

    main()