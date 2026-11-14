#include "Lander.h"
#include <iostream>



    Lander::Lander(double h , double v, double m, double mt, double t, double f, double br) {
        altitude = h;
        velocity = v;
        mass = m;
        maxThrust = mt;
        throttle = t;
        fuel = f;
        burnRate = br;
        status = FLYING;

        if (throttle > 1.0) {
            std::cout << "Warning: Throttle must be between 0.0 and 1.0. Setting throttle to 1.0." << std::endl;
            throttle = 1.0;
        }

        else if (throttle < 0.0) {
            std::cout << "Warning: Throttle must be between 0.0 and 1.0. Setting throttle to 0.0." << std::endl;
            throttle = 0.0;
        }
