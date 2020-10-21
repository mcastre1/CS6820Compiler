import re

class Stacks:
    def __init__(self):
        self.items = []
    def push(self,data):
        self.items.append(data)
    
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[-1]
    def is_empty(self):
        return self.items == []
    
    def printStack(self):
        return self.items

def infixToPostfix(inst):
    operators = ['-', '+', '*', '/', '(', '(onstack',')', '^']
    
    priority = {}
    priority['+'] = 1
    priority['-'] = 1
    priority['*'] = 2
    priority['/'] = 2
    priority['^'] = 3
    priority['('] = 4
    priority['(onstack'] = 0
    priority[')'] = 4
    
    inst = inst.split(" ")
    out = []
    st = Stacks()
    
    for i in inst:
        if(i == '('):
            st.push(i+"onstack")
        elif(i == ')'):
            while(not st.peek() == '(onstack'):
                out.append(st.pop())
            st.pop()
        elif(i in operators):
            if(st.is_empty() or priority[i] > priority[st.peek()]):
                st.push(i)
            else:
                while(not st.is_empty() and priority[i]<=priority[st.peek()]):
                    out.append(st.pop())
                st.push(i)
        else:
            out.append(i)
    while(not st.is_empty()):
        out.append(st.pop())
    
    return out