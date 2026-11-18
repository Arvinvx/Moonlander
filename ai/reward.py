def get_reward(landed, crashed, timed_out, fuel_before, fuel_after, dt, velocity, altitude, previous_altitude):

    fuel_used = fuel_before - fuel_after
    reward = 0.0
    progress = previous_altitude - altitude # How many meters the rocket moved downward during one step.

    reward -= fuel_used * 0.02  # each kg of fuel used costs 0.02 points

    reward -= dt * 0.02 # each second of flight costs 0.02 points

    if crashed:
        reward -= 100.0 + abs(velocity) * 2.0 # Crashing costs 100 points.
        # Abs make the velocitry positive so that the faster u crash the more points u lose. and that 100 is just the usual 100 for crashing.
        # The 2.0 is the multiplier for the speed of the crash so the model gives more importance to crashing at high speeds.

    if timed_out:
        reward -= 200.0 # timing out costs 200 points

    if landed:
        reward += 100.0 # landing gives 100 points

    if progress > 0: # Moving closer to the Moon earns points till we havent hit the moon.
        reward += progress * 0.02 # 

    # The closer u get to the moon the less speed


    return reward