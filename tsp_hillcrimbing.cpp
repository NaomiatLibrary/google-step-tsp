#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <assert.h>
#include <unistd.h>
#include <algorithm>
#include <errno.h> // strtol のエラー判定用

using namespace std;
// 町の構造体（今回は2次元座標）を定義
typedef struct
{
  double x;
  double y;
} City;



// プロトタイプ宣言
// distance: 2地点間の距離を計算
// solve(): TSPをといて距離を返す/ 引数route に巡回順を格納
double distance(City a, City b);
double solve(const City *city, int n, int **route_add, int *visited);
//solveの再帰用
double search(const City *city, int n, int **route_add, int *visited,int last_city);
//課題：hill climbing
double solve_hillclimbing(const City *city, int n, int *route);
double solve_hillclimbing_with_init(const City *city, int n, int **route,int shuffleN);
City *load_cities(const char* filename,int size);

City *load_cities(const char *filename,int size)
{
  City *city;
  FILE *fp;
  if ((fp=fopen(filename,"rb")) == NULL){
    fprintf(stderr, "%s: cannot open file.\n",filename);
    exit(1);
  }
  char buf[100];
  fgets(buf,100,fp);
  city = (City*)malloc(sizeof(City) * size);
  for (int i=0;i<size;i++){
    fscanf(fp,"%lf,%lf\n",&city[i].x,&city[i].y);
  }
  fclose(fp);
  return city;
}
int main(int argc, char**argv)
{
  if (argc != 4){
    fprintf(stderr, "Usage: %s <city file number> <city file size> <output file>\n", argv[0]);
    exit(1);
  }
  int n=atoi(argv[2]);
  City *city = load_cities(argv[1],n);
  FILE *fp=fopen(argv[3],"w");

  // 訪れる順序を記録する配列を設定
  int *route = NULL;
  //初期値　0->1->2->...->nのみで山登り法を行った時の解
  printf("初期値　1つのみで山登り法を行った時の解\n");
  double d = solve_hillclimbing_with_init(city,n,&route,1);
  assert(route!=NULL);
  printf("total distance = %lf\n", d);
  fprintf(fp,"index\n");
  for (int i = 0 ; i < n ; i++){
    printf("%d -> ", route[i]);
  }
  printf("0\n");
  free(route);

  //初期値をランダムに100個取って山登り法を行った時の解
  printf("初期値をランダムに100個取って山登り法を行った時の解\n");
  d = solve_hillclimbing_with_init(city,n,&route,100);
  assert(route!=NULL);
  printf("total distance = %f\n", d);
  for (int i = 0 ; i < n ; i++){
    printf("%d -> ", route[i]);
    fprintf(fp,"%d\n",route[i]);
  }
  printf("0\n");
  // 動的確保した環境ではfreeをする
  free(route);

  
  free(city);
  
  return 0;
}


double distance(City a, City b)
{
  const double dx = a.x - b.x;
  const double dy = a.y - b.y;
  return sqrt(dx * dx + dy * dy);
}


//課題：山登り方の実装
void shuffle_left0(int *array, int size) {
    // 循環した結果を避けるため、常に0番目からスタート
    for(int i = 1; i < size; i++) {
        int j = (rand()%(size-1))+1;
        int t = array[i];
        array[i] = array[j];
        array[j] = t;
    }
}
//いくつか違う初期解からはじめる。
double solve_hillclimbing_with_init(const City *city, int n, int **route,int shuffleN){
    //ランダムに初期解を取ることをsuffleN回繰り返す
    srand(100);
    double min_sum_dist=10000000.0;
    for(int i=0;i<shuffleN;i++){
        int *newroute=(int*)calloc(n,sizeof(int));
        for(int i=0;i<n;i++)newroute[i]=i;
        if(i>0)shuffle_left0(newroute,n);
        double sum_dist=solve_hillclimbing(city,n,newroute);
        /*
        printf("解%d\n",i+1);
        for (int i = 0 ; i < n ; i++)printf("%d -> ", newroute[i]);
        printf("\n合計距離\t%lf \n",sum_dist);
        */
        if(sum_dist<min_sum_dist){
            *route=newroute;
            min_sum_dist=sum_dist;
        }else{
            free(newroute);
        }
    }
    return min_sum_dist;
    
}

double solve_hillclimbing(const City *city, int n, int *route)
{
  double dist=0.0;
  for(int i=0;i<n;i++){
      dist+=distance(city[route[i]],city[route[(i+1)%n]]);
  }
  while(1){//近傍中で最短経路になるまで
    //現在のrouteについて全ての入れ替えを試す
    double min_delta_dist=0.0;

    for(int i=1;i<n-1;i++){//最初の市は0で固定しても一般性を失わない。
        for(int j=i+1;j<n;j++){
            //swap(route[i],route[j])すると、
            double delta_dist=0.0;
            //route[i-1]->route[i] が　route[i-1]->route[j]
            delta_dist-=distance(city[route[i-1]],city[route[i]]);
            delta_dist+=distance(city[route[i-1]],city[route[j]]);
            if(i+1!=j){
                //route[i]->route[i+1] が　route[j]->route[i+1]
                delta_dist-=distance(city[route[i]],city[route[i+1]]);
                delta_dist+=distance(city[route[j]],city[route[i+1]]);
                //route[j-1]->route[j] が　route[j-1]->route[i]
                delta_dist-=distance(city[route[j-1]],city[route[j]]);
                delta_dist+=distance(city[route[j-1]],city[route[i]]);
            }
            //route[j]->route[(j+1)%n] が　route[i]->route[(j+1)%n]
            delta_dist-=distance(city[route[j]],city[route[(j+1)%n]]);
            delta_dist+=distance(city[route[i]],city[route[(j+1)%n]]);
            //のみが変わるので、差分を調べる
            if(delta_dist<0){
              int tmp=route[i];
              route[i]=route[j];
              route[j]=tmp;
              dist+=delta_dist;
              min_delta_dist=min(min_delta_dist,delta_dist);
            }
            
        }
    }
    if(min_delta_dist>=0)break;//もう入れ替えが起こらない状態になれば終了
  }
  return dist;
}
