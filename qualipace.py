import csv, re
import matplotlib.pyplot as plt 
import numpy as np
#open table
intable = []
with open('C:\\Users\\Uzivatel\\Downloads\\qualipace.csv','r+',encoding='UTF-8') as f:
    reader = csv.reader(f,csv.excel)
    for row in reader:
        intable.append(row)

x_axis = []
constructors = []
for row in intable:
    #get all uniqe year/round sets
    if np.datetime64(row[0]) in x_axis:
        pass
    else:
        insert = np.datetime64(row[0])
        x_axis.append(insert)
    #get all unique constructors
    if row[2] in constructors:
        continue
    else:
        constructors.append(row[2])

for row in intable:
    for i in range(3,6):
        #loop for the qtimes
        if row[i] == '' or row[i] == '\\N':
            row[i] = 1800000 #30 mins because eh it's high enough
            continue
        else:
            m = re.match('([0-9]+):([0-9]+)\\.([0-9]+)',row[i])
            row[i] = int(m[1])*60+int(m[2])+int(m[3])/1000
    row[3] = min([row[3],row[4],row[5]])
    row = row[:4]

charttable = [] #the table that will be used to 
for item in constructors: #get all constructors in the charttable
    charttable.append([item])
    charttable.append([item]) #each constructor runs two cars
for row in charttable:
    for _ in x_axis:
        row.append('')
#now the table is prepped

for row in intable:
    #now a for loop runs for all inlist entries and inserts them at the appropriate place
    time = row[3]
    y_pos = ((constructors.index(row[2])+1)*2)-2 #from constructors shift up one, then times two and then subtract two, this will get you at the 1st constructor field, i need to do that for index 0
    x_pos = x_axis.index(np.datetime64(row[0]))+1 #add one because the first col is names
    #now we're gonna check destination and make any alterations if nescessary
    if charttable[y_pos][x_pos] != '':#field is not empty
        #there is already a time we need to see if we need to place it second or first
        if time >= charttable[y_pos][x_pos]:
            y_pos += 1
        else:
            charttable[y_pos+1][x_pos] = charttable[y_pos][x_pos] #our inserted value is lower so we need to move the old one downwards one
    charttable[y_pos][x_pos] = time #after alterations done, yeet that bitch in

#since the "no time" were used for comparison previosuly as 30m times we now yeet them back because we're done inserting
for row in charttable:
    for i in range(len(row)):
        if row[i] == 1800000 or row[i] == '':
            row[i] = None

polelist = []
#the set is now ready to be plotted, incoming are additinoal data transformations
for x in range(1,len(charttable[0])):
    for y in range(len(charttable)):
        if charttable[y][x] != None:
            pole = charttable[y][x]
            break
    for y in range(len(charttable)):
        if charttable[y][x] == None:
            continue
        elif charttable[y][x] < pole:
            pole = charttable[y][x]
    polelist.append(pole)

for x in range(1,len(charttable[0])):
    for y in range(len(charttable)):
        if charttable[y][x] == None:
            continue
        else:
            charttable[y][x] = charttable[y][x]/polelist[x-1]        

charttable.append(x_axis)
with open('C:\\Users\\Uzivatel\\Downloads\\qualiout.csv','w+') as f:
    writer = csv.writer(f)
    for y in charttable:
        writer.writerow(y)

for row in charttable:
    plt.plot_date(x_axis,row[1:],label=row[0],linestyle='-',marker=None)
plt.legend()
plt.show()
print("aa")