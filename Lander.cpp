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
        
    }

    
    bool Lander::move(double dt){

        if (dt <= 0) {
            std::cout << "Warning: Time step must be positive. No movement will occur." << std::endl;
            return false; 
        }

        if (status == LANDED || status == CRASHED) {
            return false;
        }
        
        double fuelUsed = burnRate * throttle * dt;
        
        if (fuel <= 0) {

            double acceleration = - 1.62; // Since we are out of fuel, the only acceleration is due to gravity
            velocity += acceleration * dt; // Gravity and engine changes HOW FAST
            altitude += velocity * dt; // Position changes HOW HIGH
            fuel = 0; 
            throttle = 0; 

        }else if (fuel < fuelUsed){ // if we don't have enough fuel to burn for the entire time step, we need to calculate how long the engine can run before running out of fuel
            
            double engineTime = fuel / (burnRate * throttle); // How long the engine runs. for the fuel we have 
            double remainingTime = dt - engineTime; // How much time is left after the engine runs out of fuel

            

                // ===== STAGE 1: ENGINE ON =====

            double currentThrust = maxThrust * throttle;
            double acceleration = (currentThrust / mass) - 1.62; 
            velocity += acceleration * engineTime; 
            altitude += velocity * engineTime; 

                // ===== STAGE 2: ENGINE OFF =====


            acceleration = - 1.62; // Since we are out of fuel, the only acceleration is due to gravity
            velocity += acceleration * remainingTime; // Gravity and engine changes HOW FAST
            altitude += velocity * remainingTime; // Position changes HOW HIGH
            fuel = 0; 
            throttle = 0; 
            std::cout << "Out of fuel!" << std::endl;

        
        
        }else{ // if we have enough fuel to burn for the entire time step, we can calculate the acceleration and update the velocity and altitude normally

            double currentThrust = maxThrust * throttle;
            double acceleration = (currentThrust / mass) - 1.62; 
            
            velocity += acceleration * dt; // Gravity and engine changes HOW FAST
            altitude += velocity * dt; // Position changes HOW HIGH
            fuel -= fuelUsed; // Fuel decreases based on burn rate and throttle

            if (fuel <= 0) {
                fuel = 0;
                throttle = 0;
                std::cout << "Out of fuel!" << std::endl;
            }
        
        }



        if (altitude <= 0) { // Question 1: Are we on the ground?
            altitude = 0; // Stop at the surface
            
            if (velocity < -5){ // If the lander is moving too fast more than -5 m/s, it crashes (- here means downwards) // Question 2: Did we hit too fast?
                std::cout << "CRASH! Velocity was: " << velocity << std::endl;
                velocity = 0; // Stop moving
                status = CRASHED;
            }
            
            
            else { 
                std::cout << "Safe landing! Velocity was: " << velocity << std::endl;
                velocity = 0; // Stop moving
                status = LANDED;
            }
            }

            return true;
        }

    void Lander::setThrottle(double newThrottle){

        if (fuel <= 0) {
            throttle = 0.0;
        }

        else

        if (newThrottle > 1.0) {
            throttle = 1.0;
        }

        else if (newThrottle < 0.0) {
            throttle = 0.0;
        }

        else {
            throttle = newThrottle;
        }   
    }

    double Lander::getaltitude()  {
        return altitude;
    }

    double Lander::getVelocity() {
        return velocity;
    }

    double Lander::getThrottle() {
        return throttle;
    }

    double Lander::getFuel() {
        return fuel;
    }