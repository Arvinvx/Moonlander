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
