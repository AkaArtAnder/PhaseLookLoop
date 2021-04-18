//------------------------------------------------------------------
//Discription of class Genormal methods
//------------------------------------------------------------------

#include "genormal.h"


using namespace std;
std::mutex m;


void Genormal::read_is_file()
    {
        ifstream file_mx("src/resources/generator/source/mass_X.txt");
        ifstream file_dx("src/resources/generator/source/mass_Y.txt");
        
        if (file_mx.is_open() || file_dx.is_open())
            {
                for (int count = 0; count < 99999; count++)
                    {
                        file_mx >> arr_x[count];
                        file_dx >> arr_y[count];
                    }
            }
        else cout << "File is not open" << endl;

        file_mx.close();
        file_dx.close();
    }


void Genormal::exec_generation()
    {

        int _count;
        float _uniform_value_first, _uniform_value_second, _uniform_hybrid;
        float* part_array_normal_distribution = new float[size_generation/4];

        random_device sd{};
        default_random_engine generator{ sd() };
        uniform_real_distribution<> u1(-1,1);
        uniform_real_distribution<> u2(-1,1);

        for (int count = 0; count < size_generation/4; count++)
            {
                while (true)
                    {
                        _uniform_value_first = u1(generator);
                        _uniform_value_second = u2(generator);
                        _uniform_hybrid = _uniform_value_first * _uniform_value_first  + _uniform_value_second * _uniform_value_second;
                        if ((_uniform_hybrid > 0) && (_uniform_hybrid <= 1)) break;

                    }


                if ((_uniform_hybrid >= 0.00001) && (_uniform_hybrid < 0.99999))
                    {
                        _count = (_uniform_hybrid / 0.00001) - 1;
                        part_array_normal_distribution[count] =  (arr_x[_count] + ((_uniform_hybrid - arr_y[_count]) / (arr_y[_count + 1] - arr_y[_count]))*(arr_x[_count + 1] - arr_x[_count])) * dx + mx;
                    }		
                else 
                    {
                        part_array_normal_distribution[count] = (sqrt(-2 * log(_uniform_hybrid) / _uniform_hybrid) * _uniform_value_first) *  dx + mx;
                        if (count != (size_generation/4) - 1)
                            {

                                count++;
                                part_array_normal_distribution[count] =  (sqrt(-2 * log(_uniform_hybrid) / _uniform_hybrid) * _uniform_value_second) *  dx + mx;

                            }
                    }        
            }

        m.lock();
        for(int count = 0; count < size_generation/4; count++)
            {
                array_normal_distribution.push_back(part_array_normal_distribution[count]);
            } 
        m.unlock();           
    }


vector<float> Genormal::thread_generation()
        {
            std::thread th1(&Genormal::exec_generation, this);
            std::thread th2(&Genormal::exec_generation, this);
            std::thread th3(&Genormal::exec_generation, this);
            std::thread th4(&Genormal::exec_generation, this);

            th1.join();
            th2.join();
            th3.join();
            th4.join();

            return array_normal_distribution;
        }