
# coding: utf-8

# In[1]:

import loader
import random
import numpy as np
file = '2012-Consolidated-stripped.csv'


# In[2]:

def reservoir_sample(iterator, k):
    """
    Basic reservoir sample. Takes a target sample amount
    """
    # fill the reservoir to start
    iterator = iter(iterator)
    result = [next(iterator) for _ in range(k)]
    n = k
    for item in iterator:
        n += 1
        s = random.randint(0, n)
        if s < k:
            result[s] = item
    return result

def get_sample_size(len1, len2, percent):
    return int(min(len1, len2) * percent)


# In[3]:

reload(loader)
rows = loader.load_raw(file)


# In[4]:

chronic = []
not_chronic = []
asdf = []
for pid in rows:
    person = rows[pid]
    person_data = person.info
    chron = False
    all_pop = True
    spend = 0
    for code in person.info:
        if 'chronic_'in code and not chron:
                if person_data[code] is 1:
                    chron = True
                elif person_data[code] is -9 or person_data[code] is -8 or person_data[code] is -7:
                    rows[pid].chronic = -1
        elif 'spending_pay' in code:
            spend += person_data[code]
            
    if chron:
        chronic.append(pid)
    else:
        not_chronic.append(pid)
    person.spend = spend


# In[6]:

# calculate sample size
ssize = get_sample_size(len(chronic), len(not_chronic), 0.70)

# sample chronic and non-chronic
schron = reservoir_sample(chronic, ssize)
snot = reservoir_sample(not_chronic, ssize)


# In[7]:

# get spend for each
schron_spend = [rows[pid].spend for pid in schron]
snot_spend = [rows[pid].spend for pid in snot]


# In[8]:

print(np.average(schron_spend))
print(np.average(snot_spend))


# In[ ]:



