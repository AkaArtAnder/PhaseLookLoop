#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "genormal.h"

namespace py = pybind11;

PYBIND11_MODULE(genormal, m) {
    py::class_<Genormal>(m, "Genormal")
        .def(py::init<double, double, unsigned int>())
        .def("exec_generation", &Genormal::exec_generation)
        .def("read_is_file", &Genormal::read_is_file)
        .def("thread_generation", &Genormal::thread_generation);
};