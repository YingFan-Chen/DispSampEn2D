#include <cmath>
using namespace std;

double SampEn2D(double* arr, int row, int col, int m, double r){
    long long count_m = 0, count_m1 = 0;
    for(int i = 0; i < row - m; i ++){
        for(int j = 0; j < col - m; j ++){
            for(int x = 0; x < row - m; x ++){
                for(int y = 0; y < col - m; y ++){
                    // Not compare to itself
                    if(i != x || j != y){
                        bool valid_m = true, valid_m1 = true;
                        for(int s = 0; s <= m; s ++){
                            for(int t = 0; t <= m; t ++){
                                if(abs(arr[(i + s) * col + j + t] - arr[(x + s) * col + y + t]) >= r){
                                    valid_m1 = false;
                                    if(s < m && t < m) valid_m = false;
                                }
                                if(valid_m == false) break;
                            }
                            if(valid_m == false) break;
                        }
                        if(valid_m == true) count_m ++;
                        if(valid_m1 == true) count_m1 ++;
                    }
                }
            }
        }
    }

    if(count_m1 == 0) return (double) -1;    // inf
    else if(count_m == 0) return (double) -2;   // nan
    else return -log((double) count_m1 / (double) count_m);
}

extern "C" double SampEn2DCaller(double* arr, int row, int col, int m, double r){
    return SampEn2D(arr, row, col, m, r);
}