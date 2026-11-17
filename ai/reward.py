def get_reward(landed, crashed, timed_out, fuel_before, fuel_after, dt):

    fuel_used = fuel_before - fuel_after
    reward = 0.0    

    reward -= fuel_used * 0.1  # each kg of fuel used costs 0.1 points

    reward -= dt * 0.01 # each second of flight costs 0.01 points

    if crashed : 
        reward -= 100.0 # crashing costs 100 points

    if timed_out:
        reward -= 50.0 # timing out costs 50 points

    if landed:
        reward += 100.0 # landing gives 100 points


    return reward