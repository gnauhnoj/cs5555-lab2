
# coding: utf-8

# In[99]:

get_ipython().magic(u'matplotlib inline')
import loader
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
file = '2012-Consolidated-stripped.csv'


# In[100]:

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


# in hindsight, not sure we need this (since we care about magnitude) but it's here if needed
def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)


# In[101]:

reload(loader)
rows = loader.load_raw(file)


# In[102]:

chronic = []
not_chronic = []

for pid in rows:
    person = rows[pid]
    person_data = person.info
    chron = False
    for code in person.info:
        if 'chronic_'in code and not chron:
                if person_data[code] is 1:
                    chron = True
                elif person_data[code] is -9 or person_data[code] is -8 or person_data[code] is -7:
                    rows[pid].chronic = -1
            
    if chron:
        chronic.append(pid)
    else:
        not_chronic.append(pid)
    
    person.age = person_data['demo_age']
    
    if 'spending_dist_total' in person.info:
        person.spend = person_data['spending_dist_total']
    else:
        person.spend = 0
    
    if 'service_office' in person.info:
        person.office = person_data['service_office']
    else:
        person.office = 0
        
    if 'spending_dist_office' in person.info:
        person.officesp = person_data['spending_dist_office']
    else:
        person.officesp = 0


# In[103]:

# calculate sample size
ssize = get_sample_size(len(chronic), len(not_chronic), 0.70)

# sample chronic and non-chronic
schron = reservoir_sample(chronic, ssize)
snot = reservoir_sample(not_chronic, ssize)


# In[104]:

# get spend for each
schron_spend = [rows[pid].spend for pid in schron]
snot_spend = [rows[pid].spend for pid in snot]


# In[105]:

print np.average(schron_spend), np.median(schron_spend), np.std(schron_spend)
print np.average(snot_spend), np.median(snot_spend), np.std(snot_spend)


# In[106]:

# get office visit for each
schron_office = [rows[pid].office for pid in schron]
snot_office = [rows[pid].office for pid in snot]


# In[107]:

print(np.average(schron_office))
print(np.average(snot_office))


# In[108]:

# get cost per visit for each
schron_cpv = [rows[pid].officesp/rows[pid].office for pid in schron if rows[pid].office>0]
snot_cpv = [rows[pid].officesp/rows[pid].office for pid in snot if rows[pid].office>0]


# In[109]:

print(np.average(schron_cpv))
print(np.average(snot_office))


# In[110]:

# breakdown in to age groups
chron_young, chron_mid, chron_old = [],[],[]
for pid in chronic:
    if rows[pid].age>18 and rows[pid].age<45:
        chron_young.append(pid)
    elif rows[pid].age>=45 and rows[pid].age<65:
        chron_mid.append(pid)
    elif rows[pid].age>=65:
        chron_old.append(pid)

notchron_young, notchron_mid, notchron_old = [],[],[]
for pid in not_chronic:
    if rows[pid].age>18 and rows[pid].age<45:
        notchron_young.append(pid)
    elif rows[pid].age>=45 and rows[pid].age<65:
        notchron_mid.append(pid)
    elif rows[pid].age>=65:
        notchron_old.append(pid)  


# In[111]:

# sample for each age group
def sample_age_group(chron, notchron):
    ssize_age = get_sample_size(len(chron), len(notchron), 0.7)
    schron_age = reservoir_sample(chron, ssize_age)
    snotchron_age = reservoir_sample(notchron, ssize_age)
    return schron_age, snotchron_age

schron_young, snotchron_young = sample_age_group(chron_young, notchron_young)
schron_mid, snotchron_mid = sample_age_group(chron_mid, notchron_mid)
schron_old, snotchron_old = sample_age_group(chron_old, notchron_old)


# In[112]:

print len(schron_young), len(schron_mid), len(schron_old)


# In[113]:

# gspending
chron_young_sp = [rows[pid].spend for pid in schron_young]
chron_mid_sp = [rows[pid].spend for pid in schron_mid]
chron_old_sp = [rows[pid].spend for pid in schron_old]
notchron_young_sp = [rows[pid].spend for pid in snotchron_young]
notchron_mid_sp = [rows[pid].spend for pid in snotchron_mid]
notchron_old_sp = [rows[pid].spend for pid in snotchron_old]


# In[114]:

print np.average(chron_young_sp), np.average(notchron_young_sp)
print np.average(chron_mid_sp), np.average(notchron_mid_sp)
print np.average(chron_old_sp), np.average(notchron_old_sp)


# In[115]:

chron_young_ov = [rows[pid].office for pid in chronic if rows[pid].age>18 and rows[pid].age < 45]
chron_mid_ov = [rows[pid].office for pid in chronic if rows[pid].age>=45 and rows[pid].age < 65]
chron_old_ov = [rows[pid].office for pid in chronic if rows[pid].age>=65]
notchron_young_ov = [rows[pid].office for pid in not_chronic if rows[pid].age>18 and rows[pid].age < 45]
notchron_mid_ov = [rows[pid].office for pid in not_chronic if rows[pid].age>=45 and rows[pid].age < 65]
notchron_old_ov = [rows[pid].office for pid in not_chronic if rows[pid].age>=65]


# In[116]:

print np.average(chron_young_ov), np.average(notchron_young_ov)
print np.average(chron_mid_ov), np.average(notchron_mid_ov)
print np.average(chron_old_ov), np.average(notchron_old_ov)


# In[117]:

# race

chron_white = [pid for pid in chronic if rows[pid].info['demo_race_input'] is 1]
chron_black = [pid for pid in chronic if rows[pid].info['demo_race_input'] is 2]
chron_native = [pid for pid in chronic if rows[pid].info['demo_race_input'] is 3]
chron_asian = [pid for pid in chronic if rows[pid].info['demo_race_input'] is 4]
chron_pisland = [pid for pid in chronic if rows[pid].info['demo_race_input'] is 5]
chron_multiple = [pid for pid in chronic if rows[pid].info['demo_race_input'] is 6]

notchron_white = [pid for pid in not_chronic if rows[pid].info['demo_race_input'] is 1]
notchron_black = [pid for pid in not_chronic if rows[pid].info['demo_race_input'] is 2]
notchron_native = [pid for pid in not_chronic if rows[pid].info['demo_race_input'] is 3]
notchron_asian = [pid for pid in not_chronic if rows[pid].info['demo_race_input'] is 4]
notchron_pisland = [pid for pid in not_chronic if rows[pid].info['demo_race_input'] is 5]
notchron_multiple = [pid for pid in not_chronic if rows[pid].info['demo_race_input'] is 6]

def sample_two(l1, l2, pct):
    ssize = get_sample_size(len(l1), len(l2), pct)
    s1 = reservoir_sample(l1, ssize)
    s2 = reservoir_sample(l2, ssize)
    return s1, s2

schron_white, snotchron_white = sample_two(chron_white, notchron_white, 0.7)
schron_black, snotchron_black = sample_two(chron_black, notchron_black, 0.7)
schron_native, snotchron_native = sample_two(chron_native, notchron_native, 0.7)
schron_asian, snotchron_asian = sample_two(chron_asian, notchron_asian, 0.7)
schron_pisland, snotchron_pisland = sample_two(chron_pisland, notchron_pisland, 0.7)
schron_multiple, snotchron_multiple = sample_two(chron_multiple, notchron_multiple, 0.7)
print len(schron_white), len(schron_black), len(schron_native), len(schron_asian), len(schron_pisland), len(schron_multiple)


# In[119]:

chron_white_sp, notchron_white_sp = [rows[pid].spend for pid in schron_white], [rows[pid].spend for pid in snotchron_white] 
chron_black_sp, notchron_black_sp = [rows[pid].spend for pid in schron_black], [rows[pid].spend for pid in snotchron_black] 
chron_native_sp, notchron_native_sp = [rows[pid].spend for pid in schron_native], [rows[pid].spend for pid in snotchron_native] 
chron_asian_sp, notchron_asian_sp = [rows[pid].spend for pid in schron_asian], [rows[pid].spend for pid in snotchron_asian] 
chron_pisland_sp, notchron_pisland_sp = [rows[pid].spend for pid in schron_pisland], [rows[pid].spend for pid in snotchron_pisland] 
chron_multiple_sp, notchron_multiple_sp = [rows[pid].spend for pid in schron_multiple], [rows[pid].spend for pid in snotchron_multiple] 

print 'white', np.average(chron_white_sp), np.average(notchron_white_sp)
print 'black', np.average(chron_black_sp), np.average(notchron_black_sp)
print 'native', np.average(chron_native_sp), np.average(notchron_native_sp)
print 'asian', np.average(chron_asian_sp), np.average(notchron_asian_sp)
print 'pislander', np.average(chron_pisland_sp), np.average(notchron_pisland_sp)
print 'multiple', np.average(chron_multiple_sp), np.average(notchron_multiple_sp)


# In[120]:

# diseases
hbp = []
coronary = []
myocardial = []
stroke = []
diabetes = []
asthma = []
arthritis = []
cancer = []

hbp2 = []
multiple = []

diseases = {
    'chronic_hbp': hbp, 
    'chronic_coronary': coronary, 
    'chronic_myocardial': myocardial, 
    'chronic_stroke': stroke,
    'chronic_diabetes': diabetes,
    'chronic_asthma': asthma,
    'chronic_arthritis': arthritis, 
    'chronic_cancer': cancer
}

for pid in rows:
    person = rows[pid]
    person_data = person.info
    has_chronic = False
    for code in person.info:
        if 'chronic_hbp2' in code and person_data[code] is 1:
            hbp2.append(pid)
            continue
        if code in diseases and person_data[code] is 1: 
            if not has_chronic:
                diseases[code].append(pid)
                has_chronic = True
            else:
                multiple.append(pid)
            
# get people who only have that condition
set_multiple = set(multiple)
for disease in diseases:
    setify = set(diseases[disease])
    diseases[disease] = list(setify.difference(set_multiple))

# get people who only have hbp and who were diagnosed twice
set_hbp = set(hbp)
set_hbp2 = set(hbp2)
hbp2 = list(set_hbp.intersection(set_hbp2))

# print len(multiple)
# print len(hbp2)
# print len(hbp), len(coronary), len(myocardial), len(stroke), len(diabetes), len(asthma), len(arthritis), len(cancer)


# In[121]:

def sample_single(single, pct):
    ssize = get_sample_size(len(single), sys.maxint, pct)
    sample = reservoir_sample(single, ssize)
    return sample

shbp = sample_single(hbp, 0.7)
scoronary = sample_single(coronary, 0.7)
smyocardial = sample_single(myocardial, 0.7)
sstroke = sample_single(stroke, 0.7)
sdiabetes = sample_single(diabetes, 0.7)
sasthma = sample_single(asthma, 0.7)
sarthritis = sample_single(arthritis, 0.7)
scancer = sample_single(cancer, 0.7)

shbp2 = sample_single(hbp2, 0.7)
smultiple = sample_single(multiple, 0.7)


# In[122]:

def get_spending(id_list, rows):
    return [rows[pid].info['spending_dist_total'] for pid in id_list]

shbp_sp = get_spending(shbp, rows)
scoronary_sp = get_spending(scoronary, rows)
smyocardial_sp = get_spending(smyocardial, rows)
sstroke_sp = get_spending(sstroke, rows)
sdiabetes_sp = get_spending(sdiabetes, rows)
sasthma_sp = get_spending(sasthma, rows)
sarthritis_sp = get_spending(sarthritis, rows)
scancer_sp = get_spending(scancer, rows)

shbp2_sp = get_spending(shbp2, rows)
smultiple_sp = get_spending(smultiple, rows)

print 'hbp', np.average(shbp_sp)
print 'coronary', np.average(scoronary_sp)
print 'myocardial', np.average(smyocardial_sp)
print 'stroke', np.average(sstroke_sp)
print 'diabetes', np.average(sdiabetes_sp)
print 'asthma', np.average(sasthma_sp)
print 'arthritis', np.average(sarthritis_sp)
print 'cancer', np.average(scancer_sp)

print 'hbp2', np.average(shbp2_sp)
print 'multiple', np.average(smultiple_sp)


# In[125]:

# income
schron_inc = [rows[pid].info['demo_fam_income_pl'] for pid in schron]
snotchron_inc = [rows[pid].info['demo_fam_income_pl'] for pid in snot]

# actually nevermind this isn't going to be interesting


# In[ ]:



