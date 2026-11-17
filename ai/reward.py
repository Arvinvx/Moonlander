def get_reward(landed, crashed, timed_out, fuel_before, fuel_after, dt, velocity, altitude, previous_altitude):

    fuel_used = fuel_before - fuel_after
    reward = 0.0
    progress = previous_altitude - altitude # how many meters the rocket moved downward during one step.

    reward -= fuel_used * 0.2  # each kg of fuel used costs 0.2 points

    reward -= dt * 0.02 # each second of flight costs 0.02 points

    if crashed : 
        reward -= 100.0 # crashing costs 100 points

    if timed_out:
        reward -= 100.0 # timing out costs 100 points

    if landed:
        reward += 100.0 # landing gives 100 points

    if 0 < altitude < 100 and velocity < -10: # learns to slow down when it's falling too fast near the ground, helping it land safely.
        reward -= 2.0


    if progress > 0: #Moving closer to the Moon earns points
        reward += progress * 0.02

    # The closer u get to the moon the less speed

    if altitude < 800 and velocity < -45:
        reward -= 7.0

    if altitude < 500 and velocity < -35:
        reward -= 8.0

    if altitude < 200 and velocity < -20:
        reward -= 9.0

    if altitude < 100 and velocity < -10:
        reward -= 10.0

    if altitude < 50 and velocity < -5:
        reward -= 10.0


    return reward