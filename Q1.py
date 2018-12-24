import array
import re
import copy
import time

a = array.array('d', [1.1, 3.5, 4.5])

num = input("Select data (0:project1, 1~6:graph data)\n")
if num == "0" :
    File = "hw3dataset/data.data"
else :
    File = "hw3dataset/graph_" + num + ".txt"
inputfile = open(File,"r")
arr = []
relation = []
n = 0
for line in inputfile.readlines():
    linearray = re.findall(r'[\d]+',line)	#把每個數字節錄出來
    if num == "0":
        linearray.remove(linearray[0])
    arr.append(linearray)
    for each in linearray :
        if n < int(each) :
            n = int(each)
i = 1
norm = 1    # n


########################################
#            Initialization            #
########################################
auth = [1/norm]  # 1/n instead of 1 ?
hub = [0]
pa_list = []
while i < n/2 :
    auth = auth + auth
    hub = hub + hub
    i = i * 2
while i < n :
    auth.append(1/norm)
    hub.append(0)
    i = i + 1
for i in range(0, n) :
    relation.append(hub.copy())   
for i in range(0, n) :
    pa_list.append([])

ch_num = hub.copy()
pa_num = hub.copy()
for each in arr :
    a = int(each[0])-1
    b = int(each[1])-1
    relation[a][b] = 1    #1/norm
    pa_list[b].extend([a])
    ch_num[int(each[0])-1] = ch_num[int(each[0])-1] + 1
    pa_num[int(each[1])-1] = pa_num[int(each[1])-1] + 1

most = pa_num[0]
least = pa_num[0]
for i in range(0, n) :
    if most < pa_num[i] :
        most = pa_num[i]
    if least > pa_num[i] :
        least = pa_num[i]

#print("pa_list: ", pa_list)

#print("\n------\nrelation = ", relation)


########################################
#                 HITS                 #
########################################
hub = auth
print("\n\n\n**********************")
print("|||      HITS      |||")
print("**********************\n")
#print(" 0 Time(s)\n--------------------------------")
#print("Init_Auth:", auth)
#print("Init_hub: ", hub)

# iteration
start = time.time()
error = 10.0
epsilon = 1e-4
t = 0
while error > epsilon :
    t = t + 1
    temp_a = []
    temp_h = []
    total_a = 0.0
    total_h = 0.0
    for i in range(0, n) :
        a = 0.0
        h = 0.0
        for j in range(0, n) :
            if relation[i][j] == 1 :
                h = h + auth[j]
            if relation[j][i] == 1 :
                a = a + hub[j]
        temp_a.append(a)
        temp_h.append(h)
        total_a = total_a + a
        total_h = total_h + h
    for i in range(0,n) :
        temp_a[i] = temp_a[i] / total_a
        temp_h[i] = temp_h[i] / total_h
        error = abs(auth[i] - temp_a[i]) + abs(hub[i] - temp_h[i])
    auth = temp_a.copy()
    hub = temp_h.copy()
done = time.time()
print("\n", t, " Time(s) \n--------------------------------")
print("auth: ", auth)
print("Hub: ", hub)
print("Error: ", error)
print("Time: ", done - start, "s")



########################################
#               PageRank               #
########################################
i = 1
rank = [1.0]
damping = 0.15
while i < n/2 :
    rank = rank + rank
    i = i * 2
while i < n :
    rank.append(1/norm)
    i = i + 1

print("\n\n\n**********************")
print("|||    PageRank    |||")
print("**********************\n")
#print(" 0 Time(s)\n--------------------------------")
#print("Init_PageRank: ", rank)
t = 0

start = time.time()
error = 10.0
while error > epsilon :
    t = t + 1
    error = 0.0
    buf = []
    for i in range(0, n) :
        temp = damping / n
        for j in pa_list[i] :
                temp = temp + (1 - damping) * rank[j]/ch_num[j]
        buf.append(temp)
    for i in range(0, n) :
        error = error + abs(buf[i] - rank[i])

    rank = buf.copy()
done = time.time()

print("\n", t, " Time(s)\n--------------------------------")
print("PageRank: ", rank)
print("Error: ", error)
print("Time: ", done - start, "s")



#######################################
#               SimRank               #
#######################################


if int(num) > 0 and int(num) < 6 :
    sim = []
    for i in range(0, n) :
        model = []
        for j in range(0, n) :
            if i == j :
                model.append(1.0)
            else :
                model.append(0.0)
        sim.append(model)
    model = copy.deepcopy(sim)
    #sim = copy.deepcopy(relation)
    C = 0.85

    print("\n\n\n*********************")
    print("|||    SimRank    |||")
    print("*********************")
    print("C = ", C, "\n")
    #print(" 0 Time(s)\n--------------------------------")
    #print("Init_SimRank: ", sim)

    t = 0
    start = time.time()
    error = 10.0
    while error > epsilon :
        t = t + 1
        error = 0.0
        for i in range(0, n-1) :
            for j in range(i+1, n) :
                if i == j :
                    temp = 1.0
                #elif i > j :
                #    temp = model[j][i]
                else :
                    temp = 0.0
                    if len(pa_list[i])!=0 and len(pa_list[j])!=0 :  # parent 建 list
                        for pa_i in pa_list[i] :
                            for pa_j in pa_list[j] :
                                temp = temp + sim[pa_i][pa_j]
                        temp = temp * C / ( pa_num[i] * pa_num[j] )
                error = error + abs(sim[i][j] - temp)
                model[i][j] = temp
                model[j][i] = temp
        sim = copy.deepcopy(model)
        #print("\n", t, " Time(s)\n--------------------------------")
        #print("Error: ", error)
    done = time.time()

    print("\n", t, " Time(s)\n--------------------------------")
    print("SimRank:", sim)
    print("Error: ", error)
    print("Time: ", done - start, "s")
