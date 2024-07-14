#include <unordered_map>
#include <cmath>
using namespace std;
static constexpr long long mod = 1e9 + 7, base = 337;

double DispEn2D(double* arr, int row, int col, int m_row, int m_col){
    unordered_map<int, long long> pattern;
    for(int i = 0; i <= row - m_row; i ++){
        for(int j = 0; j <= col - m_col; j ++){
            long long hash = 0;
            for(int x = 0; x < m_row; x ++){
                for(int y = 0; y < m_col; y ++){
                    hash = (hash * base + (long long) arr[(i + x) * col + j + y]) % mod;
                }
            }
            pattern[(int) hash] ++;
        }
    }

    double res = 0;
    long long total = (row - m_row + 1) * (col - m_col + 1);
    for(auto [_, count] : pattern){
        double p = (double) count / (double) total;
        res += - p * log(p);
    }

    return res;
}

double SampEn2D(double* arr, int row, int col, int m_row, int m_col, double r){
    long long count_m = 0, count_m1 = 0;
    for(int i = 0; i < row - m_row; i ++){
        for(int j = 0; j < col - m_col; j ++){
            for(int x = 0; x < row - m_row; x ++){
                for(int y = 0; y < col - m_col; y ++){
                    // Not compare to itself
                    if(i != x || j != y){
                        bool valid_m = true, valid_m1 = true;
                        for(int s = 0; s <= m_row; s ++){
                            for(int t = 0; t <= m_col; t ++){
                                if(abs(arr[(i + s) * col + j + t] - arr[(x + s) * col + y + t]) >= r){
                                    valid_m1 = false;
                                    if(s < m_row && t < m_col) valid_m = false;
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

double DispSampEn2D(double* arr, int row, int col, int m_row, int m_col){
    unordered_map<int, long long> pattern_m, pattern_m1;
    for(int i = 0; i < row - m_row; i ++){
        for(int j = 0; j < col - m_col; j ++){
            long long hash = 0;
            for(int x = 0; x < m_row; x ++){
                for(int y = 0; y < m_col; y ++){
                    hash = (hash * base + (long long) arr[(i + x) * col + j + y]) % mod;
                }
            }
            pattern_m[(int) hash] ++;

            for(int x = 0; x < m_row; x ++){
                hash = (hash * base + (long long) arr[(i + x) * col + j + m_col]) % mod;
            }
            for(int y = 0; y <= m_col; y ++){
                hash = (hash * base + (long long) arr[(i + m_row) * col + j + y]) % mod;
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

extern "C" double DispEn2DCaller(double* arr, int row, int col, int m_row, int m_col){
    return DispEn2D(arr, row, col, m_row, m_col);
}

extern "C" double SampEn2DCaller(double* arr, int row, int col, int m_row, int m_col, double r){
    return SampEn2D(arr, row, col, m_row, m_col, r);
}

extern "C" double DispSampEn2DCaller(double* arr, int row, int col, int m_row, int m_col){
    return DispSampEn2D(arr, row, col, m_row, m_col);
}
