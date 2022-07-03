#prelucrarea inputului
f = open('input.txt', 'r')
g = open('output.txt', 'w')
c = f.readlines()
n,m = c[0].split()
n,m = int(n), int(m)
tranziti = []
sigma = set()
delta_lambda = {}
nr = 0
for i in c[1:m+1]:
    nr += 1
    j = i[:-1].split()
    tranziti.append((int(j[0]),int(j[1]),j[2]))
    delta_lambda[(int(j[0]),j[2])] = int(j[1])
    if j[2] != '#':
        sigma.add(j[2])
initiala = int(c[m+1])
finale = c[m+2].split()
nf = finale[0]
finale = [int(x) for x in finale]
finale.pop(0)
ni = int(c[m+3])
inpt = []
nr = 0
for i in c[m+4:]:
    if nr != ni-1:
        inpt.append(i[:-1])
    else:
        inpt.append(i)
    nr += 1

#NodCurent este nodul curent
#calculare lambda-inchideri
ramas = [[] for i in range(n)]
lamba_inchideri = [[] for i in range(n)]
nodCurent = initiala
while nodCurent < n:
    k = 0
    nod = nodCurent
    lamba_inchideri[nodCurent].append(nodCurent)
    while k == 0 or len(ramas[nodCurent])>=0:
        for tranzitie in tranziti:
            if tranzitie[0] == nod and tranzitie[2] == '#':
                lamba_inchideri[nodCurent].append(tranzitie[1])
                ramas[nodCurent].append(tranzitie[1])
        k += 1
        if len(ramas[nodCurent])>0:
            nod = ramas[nodCurent][0]
            ramas[nodCurent].pop(0)
        else:
            break
    nodCurent += 1
# am facut un dict cu lamba-inchiderea fiecarui nod
nr = 0
inchideri_tabel = {}
for i in lamba_inchideri:
    inchideri_tabel[nr] = i
    nr += 1

#calculare dfa tabel
#primul pas
#am inceput cu lambda inchiderea nodului cu starea initiala
sigma = list(sigma)
nodCurentDfa = inchideri_tabel[0]
sigma.sort()
delta_d = {}
ce_e_de_bagat = []
multime = []
for litera in sigma:
    for nod in inchideri_tabel[0]:
        if (nod,litera) in delta_lambda.keys():
            multime.append(delta_lambda[(nod,litera)])
    for i in multime:
        for j in inchideri_tabel[i]:
            ce_e_de_bagat.append(j)
    delta_d[(tuple(inchideri_tabel[0]),litera)] = tuple(ce_e_de_bagat)
    multime = []
    ce_e_de_bagat = []

#am contiunuat cu restul tabelului
while True:
    chei = []
    for k in delta_d.keys():
        chei.append(k[0])
    for v in delta_d.values():
        if v != ():
            if v not in chei:
                multime = []
                ce_e_de_bagat = []
                nodCurent = v
                for litera in sigma:
                    for nod in nodCurent:
                        if (nod, litera) in delta_lambda.keys():
                            multime.append(delta_lambda[(nod, litera)])
                    for i in multime:
                        for j in inchideri_tabel[i]:
                            ce_e_de_bagat.append(j)
                    delta_d[(tuple(nodCurent), litera)] = tuple(ce_e_de_bagat)
                    multime = []
                    ce_e_de_bagat = []
                break
    ok = 1
    chei = []
    for k in delta_d.keys():
        chei.append(k[0])
    for v in delta_d.values():
        if v != ():
            if tuple(v) not in chei:
                ok = 0
    if ok == 1:
        break
#aici afisez functia delta pentru dfa creat din nodul de start cu litera ma duc in urmatorul nod ((start,litera) = end)
print("tranzitiile DFA-ului:")
for (k,v) in delta_d.items():
    print(k,v,sep=': ')
#calculez starile finale si starea finala
finaleDfa = []
for k in delta_d.keys():
    for f in finale:
        if f in k[0]:
            finaleDfa.append(k[0])
    if initiala in k[0]:
        initialaDfa = k[0]
finaleDfa = set(finaleDfa)
print("\nstarile finale ale DFA-ului:")
print(*finaleDfa)
print("\nstarea initiala a DFA-ului:")
print(initialaDfa)