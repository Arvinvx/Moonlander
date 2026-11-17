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
    LanderStatus status;



  public:

    Lander(double h , double v, double m, double maxThrust, double t, double f, double burnRate);

    bool move(double dt);
    
    double getaltitude() ;
    
    double getVelocity();

    double getThrottle();

    double getFuel();

    LanderStatus getStatus();

    void setThrottle(double newThrottle);

    
};
