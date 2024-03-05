#include <unordered_map>
#include <cmath>
using namespace std;
static constexpr long long mod = 1e9 + 7, base = 337;

double DispEn2D(double* arr, int row, int col, int m){
    unordered_map<int, int> pattern;
    for(int i = 0; i <= row - m; i ++){
        for(int j = 0; j <= col - m; j ++){
            long long hash = 0;
            for(int x = 0; x < m; x ++){
                for(int y = 0; y < m; y ++){
                    hash = (hash * base + (long long) arr[i * col + j]) % mod;
                }
            }
            pattern[(int) hash] ++;
        }
    }

    double res = 0;
    long long total = (row - m + 1) * (col - m + 1);
    for(auto [_, count] : pattern){
        double p = (double) count / (double) total;
        res += - p * log(p);
    }

    return res;
}

extern "C" double DispEn2DCaller(double* arr, int row, int col, int m){
    return DispEn2D(arr, row, col, m);
}