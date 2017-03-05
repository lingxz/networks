#include <vector>
#include <algorithm>
#include <iostream>
#include <set>
#include <fstream>
#include <sstream>
#include <iterator>
#include <string>
#include <cstdio>
#include <chrono>
#include <random>
#include "simplegraph/simplegraph.cpp"
#include "simplegraph/simplegraph.h"

using Clock = std::chrono::steady_clock;
using std::chrono::time_point;
using std::chrono::duration_cast;
using std::chrono::milliseconds;
//using namespace std::literals::chrono_literals;



std::vector<int> _random_subset(std::vector<int> seq, int m) {
    std::set<int> targets;
//    std::random_device rd;
//    std::mt19937 mt(rd());
//    std::uniform_int_distribution<int> dist(0, sizeof(seq)-1);
    while (targets.size() < m) {
        int randindex = rand() % sizeof(seq);
//        int randindex = *select_randomly(targets.begin(), targets.end());
//        long randindex = dist(mt);
//        cout << randindex << endl;
        targets.insert(seq[randindex]);
    }

    std::vector<int> v( targets.begin(), targets.end() );
    return v;
}


simplegraph BAGraph(int n, int m) {
    if (m < 1 || m >= n) {
        throw std::invalid_argument( "Barabási–Albert network must have m >= 1 and m < n" );
    };

    // create empty graph
    simplegraph g;
    for (int a = 0; a < m; a++){
        g.addVertex();
    }

    // create targets list
    std::vector<int> targets;
    int i = 0;
    for (i = 0; i < m; i++) {
        targets.push_back(i);
    }

    std::vector<int> repeated_nodes;

    int source = m;
    while (source < n) {
        g.addVertex();
        for (int index=0; index < targets.size(); index++) {
            g.addEdge(source, targets[index]);
        }

        repeated_nodes.insert(repeated_nodes.end(), targets.begin(), targets.end());
        for (int i = 0; i < m; i++){
            repeated_nodes.push_back(source);
        }

        targets = _random_subset(repeated_nodes, m);

        source += 1;
    }
    return g;
}

void run_ba_diff_m() {
    const char *directory = "../../data/ba/deg_dist/";
//    int m_array[6] = {1, 2, 4, 8, 16, 32};
    int m_array[1] = {4};
    int n = 10;
    for (int i = 0; i < sizeof(m_array); i++) {
        simplegraph g = BAGraph(n, m_array[i]);

        // get file path
        std::ostringstream oss;
        oss << directory << n << "_" << m_array[i] << ".txt";

        ofstream file ("../test.txt");
        for (int v=0; v < g.getNumberVertices(); v++) {
            int degree = g.getVertexDegree(v);
            if (v == g.getNumberVertices()-1) {
                file << degree;
            }
            else {
                file << degree << ",";
            }
        }
        std::cout << oss.str();
        file.close();
    }
}


int main() {
//    run_ba_diff_m();
    BAGraph(100, 4);
    std::cout << "done" << endl;
    return 0;
}
//    time_point<Clock> start = Clock::now();
//    simplegraph g = BAGraph(100, 4);
//    time_point<Clock> end = Clock::now();
//    milliseconds diff = duration_cast<milliseconds>(end - start);
//
//    std::cout << diff.count() << "ms" << endl;


//    vector<int> dd;
//    g.getDegreeDistribution(dd);
//    std::cout << dd.size() << std::endl;
//    std::cout << g.getNumberVertices() << std::endl;
//    for (std::vector<int>::const_iterator i = dd.begin(); i != dd.end(); ++i)
//        std::cout << *i << ' ';