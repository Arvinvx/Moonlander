#pragma once

enum LanderStatus {
  FLYING,
  LANDED ,
  CRASHED
}; 


class Lander {       

  private:           
    double altitude;        
    double velocity;  
    double mass;
    double maxThrust;
    double throttle; 
    double fuel;
    double burnRate;
