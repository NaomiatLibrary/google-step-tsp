# 使い方
## 山上り法
### 使い方
``` 
$gcc -o main tsp_hillcrimbing.cpp
$./main
```
### スコア
```
$./output_verifier.py
```
$N<=16$ではGreedyより悪くなってしまった。
局所最適解で大域最適解でないものが多数存在すると考えられる。
Challenge 0
output          :    3291.62
sample/random   :    3862.20
sample/greedy   :    3418.10
sample/sa       :    3291.62

Challenge 1
output          :    3778.72
sample/random   :    6101.57
sample/greedy   :    3832.29
sample/sa       :    3778.72

Challenge 2
output          :    4494.42
sample/random   :   13479.25
sample/greedy   :    5449.44
sample/sa       :    4494.42

Challenge 3
output          :   10988.77
sample/random   :   47521.08
sample/greedy   :   10519.16
sample/sa       :    8150.91

Challenge 4
output          :   17536.64
sample/random   :   92719.14
sample/greedy   :   12684.06
sample/sa       :   10675.29

Challenge 5
output          :   52876.88
sample/random   :  347392.97
sample/greedy   :   25331.84
sample/sa       :   21119.55

Challenge 6
output          :  158038.62
sample/random   : 1374393.14
sample/greedy   :   49892.05
sample/sa       :   44393.89

## Nearest neighbor+山登り法
### 使い方
solver_neighbor_hillcrimbing.pyでinput_6の問題を解き, output_6.csvに保存
```
$python3 ./solver_neighbor_hillcrimbing.py input_6.csv > output_6.csv 
```
#### greedy solverで全ての問題を解き、output_{i}.csvに保存
```
$for i in `seq 0 6`;do python3 ./solver_neighbor_hillcrimbing.py input_${i}.csv > output_${i}.csv; done
```
### スコア
Greedyより少し改善された。
```
$python3 ./output_verifier.py
```
Challenge 0
output          :    3418.10
sample/random   :    3862.20
sample/greedy   :    3418.10
sample/sa       :    3291.62

Challenge 1
output          :    3832.29
sample/random   :    6101.57
sample/greedy   :    3832.29
sample/sa       :    3778.72

Challenge 2
output          :    4821.46
sample/random   :   13479.25
sample/greedy   :    5449.44
sample/sa       :    4494.42

Challenge 3
output          :   10180.97
sample/random   :   47521.08
sample/greedy   :   10519.16
sample/sa       :    8150.91

Challenge 4
output          :   12598.21
sample/random   :   92719.14
sample/greedy   :   12684.06
sample/sa       :   10675.29

Challenge 5
output          :   24366.43
sample/random   :  347392.97
sample/greedy   :   25331.84
sample/sa       :   21119.55

Challenge 6
output          :   47989.00
sample/random   : 1374393.14
sample/greedy   :   49892.05

## Nearest neighbor+2-opt+山登り法
### 使い方
solver_neighbor_twoopt_hillcrimbing.pyでinput_6の問題を解き, output_6.csvに保存
```
$python3 ./solver_neighbor_twoopt_hillcrimbing.py input_6.csv > output_6.csv 
```
#### greedy solverで全ての問題を解き、output_{i}.csvに保存
```
$for i in `seq 0 6`;do python3 ./solver_neighbor_twoopt_hillcrimbing.py input_${i}.csv > output_${i}.csv; done
```
### スコア
2-optがない時よりかなりスコアが上昇した。
Visualizerで見たところ、確かに交差していなかった。
$N=2148$ではsa(焼きなまし法)より良いスコアが出た。
```
$python3 ./output_verifier.py
```
Challenge 0
output          :    3418.10
sample/random   :    3862.20
sample/greedy   :    3418.10
sample/sa       :    3291.62

Challenge 1
output          :    3832.29
sample/random   :    6101.57
sample/greedy   :    3832.29
sample/sa       :    3778.72

Challenge 2
output          :    4994.89
sample/random   :   13479.25
sample/greedy   :    5449.44
sample/sa       :    4494.42

Challenge 3
output          :    8970.05
sample/random   :   47521.08
sample/greedy   :   10519.16
sample/sa       :    8150.91

Challenge 4
output          :   11489.79
sample/random   :   92719.14
sample/greedy   :   12684.06
sample/sa       :   10675.29

Challenge 5
output          :   21384.20
sample/random   :  347392.97
sample/greedy   :   25331.84
sample/sa       :   21119.55

Challenge 6
output          :   42623.76
sample/random   : 1374393.14
sample/greedy   :   49892.05
sample/sa       :   44393.89

## MST->2-opt->山登り
最小全域木の考え方を用いる、クリストフィードのアルゴリズムを用いた。 
この近似アルゴリズムの出力は、最適解の重みの3/2以下になることが保証されている。
### 使い方
input_6の問題を解き, output_6.csvに保存
```
$python3 ./solver_MST.py input_6.csv > output_6.csv 
```
全ての問題を解き、output_{i}.csvに保存
```
$for i in `seq 0 6`;do python3 ./solver_MST.py input_${i}.csv > output_${i}.csv; done
```
### スコア
Nが大きい問題ではsa(焼きなまし法)より良いスコアが出た。
また、去年のChallenge 6のベスト・スコア（41661.92）を超えた。(41530.57)
```
$python3 ./output_verifier.py
```

Challenge 0
output          :    3291.62
sample/random   :    3862.20
sample/greedy   :    3418.10
sample/sa       :    3291.62

Challenge 1
output          :    3832.29
sample/random   :    6101.57
sample/greedy   :    3832.29
sample/sa       :    3778.72

Challenge 2
output          :    4494.42
sample/random   :   13479.25
sample/greedy   :    5449.44
sample/sa       :    4494.42

Challenge 3
output          :    8612.75
sample/random   :   47521.08
sample/greedy   :   10519.16
sample/sa       :    8150.91

Challenge 4
output          :   10886.05
sample/random   :   92719.14
sample/greedy   :   12684.06
sample/sa       :   10675.29

Challenge 5
output          :   20807.97
sample/random   :  347392.97
sample/greedy   :   25331.84
sample/sa       :   21119.55

Challenge 6
output          :   41530.57
sample/random   : 1374393.14
sample/greedy   :   49892.05
sample/sa       :   44393.89