#include <pybind11/pybind11.h>
#include "Lander.h"

namespace py = pybind11;

PYBIND11_MODULE(lander_cpp, m) {

    py::enum_<LanderStatus>(m, "LanderStatus")
    .value("FLYING", FLYING)
    .value("LANDED", LANDED)
    .value("CRASHED", CRASHED);


    py::class_<Lander>(m, "Lander") // expose the Lander class to Python
        .def(py::init<double, double, double, double,
                      double, double, double>())
        .def("move", &Lander::move) // expose the move method to Python and the codes below do the same but different methods
        .def("get_altitude", &Lander::getaltitude)
        .def("get_velocity", &Lander::getVelocity)
        .def("get_fuel", &Lander::getFuel)
        .def("get_throttle", &Lander::getThrottle)
        .def("set_throttle", &Lander::setThrottle)
        .def("get_status", &Lander::getStatus);
}
