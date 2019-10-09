#    Znajdowanie najkrótszej trasy komiwojażera dla 51 dużych miast w Polsce
#    Napisane na potrzeby wykładu popularnonaukowego w ramach Festiwalu Nauki oraz artykułu dla miesięcznika Delta
  
#    Copyright (C) Łukasz Kowalik 2019, Uniwersytet Warszawski, Wydział Matematyki, Informatyki i Mechaniki.

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>. 


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import csv
from pulp import *

# inicjalizujemy mapowanie współrzędnych geograficznych
map = Basemap(llcrnrlon=13,llcrnrlat=48.5,urcrnrlon=25,urcrnrlat=55,
             resolution='i', projection='tmerc', lat_0 = 52, lon_0 = 19)

# wczytujemy współrzędne i nazwy 51 miast
with open('data/polska-51-coor.csv',encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    cities = []
    coor = []
    pos = []
    for row in readCSV:
        cities.append(row[0])
        x,y = map(float(row[2]),float(row[1]))
        coor.append((x,y))
        pos.append((row[3],row[4]))
            
# wczytujemy tabelę odległości drogowych
with open('data/polska-51-dist.csv',encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    first = True
    dist = []
    for row in readCSV:
        if first:
            first = False
        else:    
            num_row = []
            for s in row[1:]:
                num_row.append(float(s))
            dist.append (num_row)
            
n = len(cities)

sym = [[(min(i,j),max(i,j)) for j in range (n)] for i in range (n)]

# definiujemy program liniowy
prob = LpProblem("TSP", LpMinimize)

# nasz program ma zmiaenną x_(i,j) dla każdego 0<=i<j<=n, o wartościach w przedziale [0,1]
var = LpVariable.dicts("x", [(i,j) for i in range(n) for j in range(i+1,n)], 0, 1, cat="Continuous")

# funkcja celu
prob += lpSum(dist[i][j]*var[(i,j)] for i in range(n) for j in range(i+1,n))

# warunki, które mówią, że suma wszystkich zmiennych dla połączeń o końcu w jednym mieście wynosi 2
for i in range(n):
    prob += lpSum(var[sym[i][j]] for j in range(n) if j != i) == 2

done = False
cnt = 0

def iter():

    global cnt,sym,cities,coor,prob,fig,plt
 
    if cnt < 5: cnt += 1
    if cnt == 2:
        #krok 2: dodajemy 7 warunków eliminacji podtras
        for S in [[14,33,41],[2,6,13],[32,34,18],[17,24,42,48],[12,15,36],[4,21,49],[11,44,19]]:
            prob += lpSum (var[sym[S[i]][S[j]]] for i in range(len(S)) for j in range(i+1,len(S))) <= len(S) - 1
    elif cnt == 3:             
        #krok 3: dodajemy 2 warunki eliminacji podtras
        for S in [[2,6,13,17,42,24,48],[4,21,0,35,45,37,33,14,41,34,18,32,49]]:
            prob += lpSum (var[sym[S[i]][S[j]]] for i in range(len(S)) for j in range(i+1,len(S))) <= len(S) - 1     
    elif cnt == 4:
        #krok 4: dodajemy 1 warunek eliminacji podtras
        for S in [[11,19,44,47]]:
            prob += lpSum (var[sym[S[i]][S[j]]] for i in range(len(S)) for j in range(i+1,len(S))) <= len(S) - 1     
    elif cnt == 5:        
        #krok 5: dodajemy warunek 2-skojarzeniowy
        for (H,T) in [([19,20,50],[(19,11),(50,10),(20,31)])]:
            prob += lpSum (var[sym[H[i]][H[j]]] for i in range(len(H)) for j in range(i+1,len(H))) + \
                    lpSum (var[sym[i][j]] for (i,j) in T) <= len(H) + len(T) // 2

    #rozwiązywanie programu liniowego
    prob.solve()    

    # wczytywanie konturu Polski
    fig.clear()
    map.readshapefile("data/gadm36_POL_0", "Poland", linewidth=1)

    n = len(cities)

    # rysowanie trasy
    for i in range(n): 
        for j in range(i+1,n):
            if var[(i,j)].varValue == 1:
                plt.plot([coor[i][0], coor[j][0]],[coor[i][1], coor[j][1]],color='black',lw=1)
            elif var[(i,j)].varValue == 0.5:
                plt.plot([coor[i][0], coor[j][0]],[coor[i][1], coor[j][1]],linestyle='dashed',color='red',lw=1)
            elif var[(i,j)].varValue > 0:        
                plt.plot([coor[i][0], coor[j][0]],[coor[i][1], coor[j][1]],color='blue',lw=1)
                    
    for i in range(n):
        if cnt < 5:
            map.plot(coor[i][0],coor[i][1],marker='o',color='black',mfc="white",markersize=11)
            plt.text(coor[i][0],coor[i][1]-3000, str(i),fontsize=8,ha="center",va="center",color='black',stretch='condensed')
        else:    
            map.plot(coor[i][0],coor[i][1],marker='o',color='black',markersize=3)
            plt.text(coor[i][0],coor[i][1], cities[i],fontsize=8,ha=pos[i][0],va=pos[i][1],color='black',stretch='condensed')
            fig.canvas.set_window_title('Znaleziono trasę optymalną. Zamnij okno.') 


    ax = plt.gca()
    ax.axis('off')
    plt.text(0.2,0.1,str(round(value(prob.objective),3))+" km", color='black',transform=ax.transAxes)

    fig.canvas.draw()
    fig.savefig("tsp"+str(cnt)+".pdf", bbox_inches='tight')

def press(event):
    sys.stdout.flush()
    iter()

fig = plt.figure(frameon = False)
fig.canvas.set_window_title('Naciśnij dowolny klawisz aby wykonać kolejny krok') 
fig.canvas.mpl_connect('key_press_event', press)
plt.show()



