#include <iostream>
#include <vector>
#include "ann/Network.h"

int main() {
    std::vector<int> arch; 
    arch.push_back(80);
    arch.push_back(60);
    arch.push_back(35);
    Network* n = new Network(arch);

    return 0;
}
