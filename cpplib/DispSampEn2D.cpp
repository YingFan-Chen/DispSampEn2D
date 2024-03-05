#include <unordered_map>
#include <cmath>
using namespace std;
static constexpr long long mod = 1e9 + 7, base = 337;

double DispSampEn2D(double* arr, int row, int col, int m){
    unordered_map<int, int> pattern_m, pattern_m1;
    for(int i = 0; i < row - m; i ++){
        for(int j = 0; j < col - m; j ++){
            long long hash = 0;
            for(int x = 0; x < m; x ++){
                for(int y = 0; y < m; y ++){
                    hash = (hash * base + (long long) arr[i * col + j]) % mod;
                }
            }
            pattern_m[(int) hash] ++;
            
            for(int x = 0; x < m; x ++){
                hash = (hash * base + (long long) arr[(i + x) * col + j + m]) % mod;
            }
            for(int y = 0; y <= m; y ++){
                hash = (hash * base + (long long) arr[(i + m) * col + j + y]) % mod;
            }
            pattern_m1[(int) hash] ++;
        }
    }

    long long count_m = 0, count_m1 = 0;
    for(auto [_, count] : pattern_m){
        count_m += (count) * (count - 1);
    }
    for(auto [_, count] : pattern_m1){
        count_m1 += (count) * (count - 1);
    }

    if(count_m1 == 0) return (double) -1;    // inf
    else if(count_m == 0) return (double) -2;   // nan
    else return - log((double) count_m1 / (double) count_m);
}

extern "C" double DispSampEn2DCaller(double* arr, int row, int col, int m){
    return DispSampEn2D(arr, row, col, m);
}