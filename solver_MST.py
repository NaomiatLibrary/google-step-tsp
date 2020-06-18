#!/usr/bin/env python3
from __future__ import print_function
import sys
import math
import itertools
from common import print_tour, read_input
import copy
#debug用
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def greedy_tour(cities,N,dist):
    #0から開始して最も近い頂点から順に辿っていく
    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour

def hillcrimbing(cities,N,dist,tour):
    while True:#近傍中で最短経路になるまで現在のrouteについて全ての入れ替えを試す
        min_delta_dist=0.0
        for i in range(1,N-1):#最初の市は0で固定するので1~N-1
            for j in range(i+1,N):
                #swap(tour[i],tour[j])すると、
                delta_dist=0.0
                #route[i-1]->route[i] が　route[i-1]->route[j]に
                delta_dist-=dist[tour[i-1]][tour[i]]
                delta_dist+=dist[tour[i-1]][tour[j]]
                if(i+1!=j):
                    #route[i]->route[i+1] が　route[j]->route[i+1]
                    delta_dist-=dist[tour[i]][tour[i+1]]
                    delta_dist+=dist[tour[j]][tour[i+1]]
                    #route[j-1]->route[j] が　route[j-1]->route[i]
                    delta_dist-=dist[tour[j-1]][tour[j]]
                    delta_dist+=dist[tour[j-1]][tour[i]]
                #route[j]->route[(j+1)%n] が　route[i]->route[(j+1)%n]
                delta_dist-=dist[tour[j]][tour[(j+1)%N]]
                delta_dist+=dist[tour[i]][tour[(j+1)%N]]
                #のみが変わるので、差分を調べ、小さくなるときは入れ替える
                if(delta_dist<0.0):
                    tour[i],tour[j]=tour[j],tour[i]
                    min_delta_dist=min(min_delta_dist,delta_dist)
        eprint(str(min_delta_dist))#debug
        if min_delta_dist>=0:
            break;#もう入れ替えが起こらない状態になれば終了

def swap_edges(tour,start,end):
    #tourの[start,end]を入れ替える
    left=start
    right=end
    while left<right:
        tour[left],tour[right]=tour[right],tour[left]
        left+=1
        right-=1

def two_opt(cities,N,dist,tour):
    #tour[i-1]->tour[i]とtour[j]->tour[(j+1)%N]の先を交換(i=1,2,3... j=i+1,...N-1)
    while True:
        epsilon=-0.1 #誤差により全く同じ回路が0にならないことがあるので…
        min_delta_dist=epsilon
        for i in range(1,N-1):#最初の市は0で固定するので1~N-1
            for j in range(i+1,N):
                delta_dist=0.0
                delta_dist-=dist[tour[i-1]][tour[i]]
                delta_dist-=dist[tour[j]][tour[(j+1)%N]]
                delta_dist+=dist[tour[i-1]][tour[j]]
                delta_dist+=dist[tour[i]][tour[(j+1)%N]]
                min_delta_dist=min(min_delta_dist,delta_dist)
                if delta_dist<epsilon:
                    swap_edges(tour,i,j)
        if min_delta_dist>=epsilon:
            break

#MSTを作るためのunion_find
class Union_Find():
    def __init__(self,n):
        self.n=n
        self.parents=[-1]*n
        self.rank=[0]*n
    def find(self,x):#根を返す
        if self.parents[x]<0:
            return x
        else:
            self.parents[x]=self.find(self.parents[x])
            return self.parents[x]
    def unite(self,x,y):
        x=self.find(x)
        y=self.find(y)
        if x==y:
            return
        if self.rank[x]<self.rank[y]:
            self.parents[x]=y
        else:
            self.parents[y]=x
        if self.rank[x]==self.rank[y]:
            self.rank[x]+=1
    def same(self,x,y):
        return self.find(x)==self.find(y)

def kruskal(N,dist):
    #クラスカル法による最小全域木(MST)の生成　計算量(V^2logV)
    edges=[]
    for i in range(N-1):#全ての辺の組み合わせをedgesに入れる
        for j in range(i+1,N):
            edges.append((dist[i][j],i,j))
    #辺の長さでソート
    edges.sort()
    mst={k:[] for k in range(N)}
    uf=Union_Find(N)
    #辺の長さが短い順に取り出し、連結して最小全域木を作る
    for cost,a,b in edges:
        if uf.same(a,b)==False:#連結成分でない場合
            mst[a].append(b)#辺をmstに追加
            mst[b].append(a)
            uf.unite(a,b)#連結する
    #木を返す
    return mst

import networkx as nx
def min_weight_perfect_matching(O,dist):
    #Oに含まれる頂点のみからなるグラフから最小重み最適マッチングMをもとめる
    K=len(O)
    #Oのなかの全ての二頂点対を列挙
    combis=list(itertools.combinations(O,2))
    #最小重み最適マッチングを求める(networkx を使用)
    #networkxを使わないでも実装してみたい…！（BlossomのアルゴリズムやHungarianアルゴリズムなどがあるが、実装が大変そう）
    weight = [dist[c[0]][c[1]] for c in combis]
    edge_weight = [(combis[i][0], combis[i][1], {'weight': -weight[i]}) for i in range(len(combis))]
    G = nx.Graph(edge_weight)
    M = nx.max_weight_matching(G, True, 'weight')
    M = [list(m) for m in M]
    G.clear()
    return M

    

def christofides(N,dist,mst):
    #MSTをもとに
    #mstに含まれる奇数次の頂点集合Oを作成する
    O=[k for k,v in mst.items() if len(v)%2==1]
    #多分偶数になる気がする
    assert(len(O)%2==0)
    #Oに含まれる頂点によって与えられる誘導部分グラフを作成
    #その部分誘導グラフにおいて最適マッチング(完全マッチングのうち最も辺の長さの合計が小さいもの)Mgを探索する。
    Mg=min_weight_perfect_matching(O,dist)
    #MとMSTの辺を統合し、すべての頂点が偶数次となる多重グラフHgを構築する。
    Hg=copy.deepcopy(Mg)#辺の集合
    for k,v_list in mst.items():
        for v in v_list:
            if k<v:
                Hg.append([k,v])
    #H内部でオイラー閉路を構成する
    eular_tour=[0,]#0を始点とする
    while len(Hg):
        for e in Hg:
            if eular_tour[-1]==e[0]:
                eular_tour.append(e[1])
                Hg.remove(e)
            elif eular_tour[-1]==e[1]:
                eular_tour.append(e[0])
                Hg.remove(e)
        if eular_tour[0]==eular_tour[-1]:#戻ってきたとき
            #閉路の端をちょっとずらしてみる
            eular_tour=[eular_tour[-2]]+eular_tour[:-1]
    #構成したオイラー閉路において、既に訪れた点を飛ばしながら辿る（近道）
    #ことにより、ハミルトン閉路を形成する。
    tour=[]
    visited=[False]*N
    for et in eular_tour:
        if visited[et]==False:
            tour.append(et)
            visited[et]=True
    assert(len(tour)==N)
    return tour




def solve(cities):
    N = len(cities)

    #距離の計算
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    mst=kruskal(N,dist)
    tour=christofides(N,dist,mst)
    #tour=greedy_tour(cities,N,dist)
    eprint("chiristofides done")
    two_opt(cities,N,dist,tour)
    eprint("2-opt end")
    hillcrimbing(cities,N,dist,tour)
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
