// Header file descriptor class generator normal destribution

#pragma once

#include <iostream>
#include <random>
#include <cmath>
#include <vector>
#include <fstream>
#include <thread>
#include <mutex>

using namespace std;

    class Genormal
    {
        private:

            vector <float> array_normal_distribution;
            double arr_x[99999];
            double arr_y[99999];
            double mx, dx;
            int size_generation;
        
        public:

            Genormal(double mx_value, double dx_value, unsigned int size)
                {
                    mx = mx_value;
                    dx = dx_value;
                    size_generation = size;
                    read_is_file(); 
                }

            void exec_generation();

            void read_is_file();

            vector<float> thread_generation();
    };