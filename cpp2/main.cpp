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
#include "simplegraph/simplegraph.cpp"
#include "simplegraph/simplegraph.h"

using namespace std;

using Clock = std::chrono::steady_clock;
using std::chrono::time_point;
using std::chrono::duration_cast;
using std::chrono::milliseconds;
//using namespace std::literals::chrono_literals;

template<class bidiiter>
bidiiter random_unique(bidiiter begin, bidiiter end, size_t num_random) {
    size_t left = std::distance(begin, end);
    while (num_random--) {
        bidiiter r = begin;
        std::advance(r, rand()%left);
        std::swap(*begin, *r);
        ++begin;
        --left;
    }
    return begin;
}

std::vector<int> random_subset(std::vector<int> seq, int m) {
    std::set<int> targets;

//    std::random_device rd;
//    std::mt19937 mt(rd());
//    std::uniform_int_distribution<int> dist(0, seq.size()-1);
    int max;
    if (10 * m > seq.size()) {
        max = seq.size();
    } else {
        max = 10 * m;
    }
    random_unique(seq.begin(), seq.end(), max);
    int i = 0;
    while (targets.size() < m) {
//        int randindex = rand() % seq.size();
//        int randindex = *select_randomly(targets.begin(), targets.end());
//        int randindex = dist(mt);
        targets.insert(seq[i]);
        i++;
    }

    std::vector<int> v(targets.size());
//    std::copy(targets.begin(), targets.end(), v.begin());
    v.assign(targets.begin(), targets.end());

//    for (std::vector<int>::const_iterator i = v.begin(); i != v.end(); ++i)
//        std::cout << *i << ' ';
//    cout << "\nend" << endl;
    return v;
}

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


void run_ba_diff_m() {
    const char *directory = "../../data/ba/deg_dist/";
//    int m_array[6] = {1, 2, 4, 8, 16, 32};
    int m_array[1] = {4};
    int n = 100000;
    for (int i = 0; i < 1; i++) {
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

int main() {
    run_ba_diff_m();

//    time_point<Clock> start = Clock::now();
//    simplegraph g = BAGraph(100, 4);
//    Barabasi(4, 100000);
//    time_point<Clock> end = Clock::now();
//    milliseconds diff = duration_cast<milliseconds>(end - start);
//
//    std::cout << diff.count() << "ms" << endl;

//    vector<int> dd;
//    g.getDegreeDistribution(dd);
//    for (std::vector<int>::const_iterator i = dd.begin(); i != dd.end(); ++i)
//        std::cout << *i << ' ';

    std::cout << "done" << endl;
    return 0;
}
