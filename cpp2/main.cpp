#include <vector>
#include <algorithm>
#include <iostream>
#include <set>
#include <fstream>
#include <sstream>
#include <iterator>
#include <string>
#include <cstdio>
#include <time.h>
#include <stdlib.h>
#include <chrono>
#include <random>
#include <cstdlib>
#include <time.h>
#include <windows.h>
#include "simplegraph/simplegraph.cpp"
#include "simplegraph/simplegraph.h"

using namespace std;

using Clock = std::chrono::steady_clock;
using std::chrono::time_point;
using std::chrono::duration_cast;
using std::chrono::milliseconds;
//using namespace std::literals::chrono_literals;


simplegraph BAGraph(int n, int m) {
    simplegraph g;
    std::random_device rd;     // only used once to initialise (seed) engine
    std::mt19937 rng(rd());    // random-number engine used (Mersenne-Twister in this case)

    vector<int> M(2*n*m);
    for (int v = 0; v < n; v++) {
        g.addVertex();
        for (int i = 0; i < m; i++) {
            M[2*(v*m + i)] = v;
            std::uniform_int_distribution<int> uni(0, 2*(v*m+i)+1);
//            int r = rand() % 2*(v*m+i)+1;
            auto r = uni(rng);
            M[2*(v*m + i) + 1] = M[r];
        }
    }
    for (int i = 0; i < n*m; i++) {
        g.addEdge(M[2*i], M[2*i+1]);
    }
    return g;
}

simplegraph RAGraph(int n, int m) {
    simplegraph g;
    std::random_device rd;     // only used once to initialise (seed) engine
    std::mt19937 rng(rd());    // random-number engine used (Mersenne-Twister in this case)

    for (int v = 0; v < n; v++) {
        g.addVertex();
        for (int i = 0; i < m; i++) {
            std::uniform_int_distribution<int> uni(0, v);
            auto r = uni(rng);
            g.addEdge(v, r);
        }
    }
}

void run_ba_diff_m(int n, string s) {
    const string directory = "../../data/ba/deg_dist" + s + '/';
    //Make the directory if it doesn't exist
    string s1 = "mkdir ";
    string s2 = "../../data/ba/deg_dist";
    system((s1 + s2 + s).c_str());
    int m_array[6] = {1, 2, 4, 8, 16, 32};
    for (int i = 0; i < 6; i++) {
        simplegraph g = BAGraph(n, m_array[i]);

        // get file path
        std::ostringstream oss;
        oss << directory << n << "_" << m_array[i] << ".txt";

        ofstream file (oss.str());
        for (int v=0; v < g.getNumberVertices(); v++) {
            int degree = g.getVertexDegree(v);
            if (v == g.getNumberVertices()-1) {
                file << degree;
            }
            else {
                file << degree << ",";
            }
        }
        file.close();
    }
}

void run_ba_diff_n(int m, string s) {
    const string directory = "../../data/ba/deg_dist" + s + '/';
    //Make the directory if it doesn't exist
    string s1 = "mkdir ";
    string s2 = "../../data/ba/deg_dist";
    system((s1 + s2 + s).c_str());
    int n_array[6] = {100, 1000, 10000, 100000, 1000000, 10000000};
    for (int i = 0; i < 6; i++) {
        simplegraph g = BAGraph(n_array[i], m);

        // get file path
        std::ostringstream oss;
        oss << directory << n_array[i] << "_" << m << ".txt";

        ofstream file (oss.str());
        for (int v=0; v < g.getNumberVertices(); v++) {
            int degree = g.getVertexDegree(v);
            if (v == g.getNumberVertices()-1) {
                file << degree;
            }
            else {
                file << degree << ",";
            }
        }
        file.close();
    }
}

vector<int> generate_synthetic(int m, int max, int N) {
    // Setup the random bits
    std::random_device rd;
    std::mt19937 gen(rd());
    vector<float> weights(max);
    for (int k = 0; k < max; k++) {
        if (k < m) {
            weights[k] = 0;
        } else {
            float a = 2 * float(m) * (float(m) + 1) / (float(k) * (float(k) + 1) * (float(k) + 2));
            weights[k] = a;
        }
    }

    // Create the distribution with those weights
    std::discrete_distribution<> d(weights.begin(), weights.end());
    vector<int> degrees(N);
    for (int n = 0; n < N; n++) {
        int number = d(gen);
        degrees[n] = number;
    }
    return degrees;
}

void generate_synthetic_wrapper(int m, int max, int N) {
    const string directory = "../../data/ba/synthetic/";
    //Make the directory if it doesn't exist
    string s1 = "mkdir ";
    string s2 = "../../data/ba/synthetic";
    system((s1 + s2).c_str());

    for (int i=0; i < 25; i++) {
        // get file path
        std::ostringstream oss;
        oss << directory << N << "_" << m << "_" << i <<".csv";
        ofstream file (oss.str());
        vector<int> v = generate_synthetic(m, max, N);
        std::copy(v.begin(), v.end(), std::ostream_iterator<int>(file, ","));
    }
}

int main() {
//    generate_synthetic_wrapper(1, 3027, 1000000);
//    generate_synthetic_wrapper(2, 5195, 1000000);
//    generate_synthetic_wrapper(4, 10916, 1000000);
//    generate_synthetic_wrapper(8, 20417, 1000000);
//    generate_synthetic_wrapper(16, 33887, 1000000);
//    generate_synthetic_wrapper(32, 64985, 1000000);

//    generate_synthetic_wrapper(32, 16569, 100000);
    for (int i=21;  i<=100; i++) {
        string s = std::to_string(i);
        run_ba_diff_m(1000000, s);
    }
//    run_ba_diff_m(100000, "1");

//    time_point<Clock> start = Clock::now();
//    simplegraph g = BAGraph(100, 4);
//    time_point<Clock> end = Clock::now();
//    milliseconds diff = duration_cast<milliseconds>(end - start);

//    std::cout << diff.count() << "ms" << endl;

//    vector<int> dd;
//    g.getDegreeDistribution(dd);
//    for (std::vector<int>::const_iterator i = dd.begin(); i != dd.end(); ++i)
//        std::cout << *i << ' ';

    std::cout << "done" << endl;
    return 0;
}
