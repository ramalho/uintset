#!/usr/bin/env python
# coding: utf-8

# # Undertanding `uintset`

# In[1]:


from uintset import UintSet

def dump(u):
    top = '┌' + '─┬' * len(bin(u._bits)[3:]) + '─┐'
    bits = '│' + '│'.join(list(bin(u._bits)[2:])) + '│'
    bottom = '└' + '─┴' * len(bin(u._bits)[3:]) + '─┘'
    #print(f'{u} → {u._bits}\n{bits:>64}\n{bottom:>64}')
    print(f'{u} → {u._bits}\n{bin(u._bits)[2:]}')


# In[2]:


empty = UintSet()
dump(empty)


# In[3]:


zero = UintSet([0])
dump(zero)


# In[4]:


one = UintSet([1])
dump(one)


# In[5]:




# In[6]:


# In[7]:


five_elements = UintSet([0, 1, 2, 4, 8])
dump(five_elements)

first_10 = UintSet(range(10))
dump(first_10)

ten = UintSet([10])
dump(ten)


# In[8]:




# In[9]:


evens = UintSet(range(0, 20, 2))
dump(evens)


# In[10]:


odds = UintSet(range(1, 20, 2))
dump(odds)

twenty_five = UintSet([25])
dump(twenty_five)

# In[11]:


sixty = UintSet([60])
dump(sixty)


# In[12]:

from random import randrange

elems = []
e = 0
while True:
    e += randrange(1, 20)
    if e > 300:
        break
    elems.append(e)

n_elements = UintSet(elems)
dump(n_elements)

dump(UintSet([290]))

