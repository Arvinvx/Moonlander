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

        if (mass <= 0) {
            std::cout << "Warning: Mass must be positive. Setting mass to 1000.0." << std::endl;
            mass = 1000.0;
        }

        if (maxThrust <= 0) {
            std::cout << "Warning: Max thrust must be positive. Setting max thrust to 1000.0." << std::endl;
            maxThrust = 1000.0;
        }
        
        if (burnRate <= 0){
            std::cout << "Warning: Burn rate must be positive. Setting burn rate to 1.0." << std::endl;
            burnRate = 1.0;
        }

        if (fuel < 0) {
            std::cout << "Warning: Fuel cannot be negative. Setting fuel to 0." << std::endl;
            fuel = 0;
        }
