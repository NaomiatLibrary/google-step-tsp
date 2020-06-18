#!/usr/bin/env python3
from __future__ import print_function
import sys
import math

from common import print_tour, read_input

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
        #eprint("hello")#debug
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

def solve(cities):
    N = len(cities)

    #距離の計算
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    tour=greedy_tour(cities,N,dist)
    two_opt(cities,N,dist,tour)
    eprint("2-opt end")
    hillcrimbing(cities,N,dist,tour)
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
