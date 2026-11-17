def get_reward(landed, crashed, timed_out, fuel_before, fuel_after, dt, velocity, altitude, previous_altitude):

    fuel_used = fuel_before - fuel_after
    reward = 0.0
    progress = previous_altitude - altitude # how many meters the rocket moved downward during one step.

    reward -= fuel_used * 0.02  # each kg of fuel used costs 0.02 points

    reward -= dt * 0.02 # each second of flight costs 0.02 points

    if crashed:
        reward -= 100.0 + abs(velocity) * 2.0 # Crashing costs 100 points.
        # Abs make the velocitry positive so that the faster u crash the more points u lose. and that 100 is just the usual 100 for crashing.
        # The 2.0 is the multiplier for the speed of the crash so the model gives more importance to crashing at high speeds.

    if timed_out:
        reward -= 100.0 # timing out costs 100 points

    if landed:
        reward += 100.0 # landing gives 100 points

    if progress > 0: #Moving closer to the Moon earns points
        reward += progress * 0.02

    # The closer u get to the moon the less speed

 

    if altitude < 50 and velocity < -5:
        reward -= 10.0

    elif altitude < 100 and velocity < -10:
         reward -= 10.0
    
    elif altitude < 200 and velocity < -20:
        reward -= 9.0

    elif altitude < 500 and velocity < -35:
        reward -= 8.0

    elif altitude < 800 and velocity < -45:
        reward -= 7.0


    return reward