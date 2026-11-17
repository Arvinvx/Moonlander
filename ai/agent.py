import torch
import torch.nn as nn
import os
import shutil
from reward import get_reward
 
dll_dir = os.path.dirname(shutil.which("g++"))
handle = os.add_dll_directory(dll_dir)


import lander_cpp

scale = torch.tensor([1000.0, 100.0, 500.0])


model = nn.Sequential(
    nn.Linear(3, 32),
    nn.ReLU(), # turns the 32 if positive make it positive if negative make it 0.
    nn.Linear(32, 1),
    nn.Sigmoid()    
    )

counter = 0
total_reward = 0.0

for i in range(100):

    rocket = lander_cpp.Lander( # we moved it from outside for loop because we want to create a new rocket for each iteration of the loop.
    1000, -50, 1000, 3000, 0.2, 500, 2
    )


    counter = 0
    total_reward = 0.0

    while rocket.get_altitude() > 0 and counter < 300:

        counter += 1

        state = torch.tensor(
        [
            rocket.get_altitude(),
            rocket.get_velocity(),
            rocket.get_fuel()
        ],
        dtype=torch.float32
        )

        print(state)
        print(state.shape) # Shows how many values the tensor contains.
        
        normalized_state = state / scale
        output = model(normalized_state)


        throttle = output.item() # here we ask ai to give us a value between 0 and 1 (thrust).
        rocket.set_throttle(throttle) # we set the throttle to the value given by the ai model (we send the throttle to c++).
        fuel_before = rocket.get_fuel() # before move because we need to compare fuel before and after movement to calculate how much was burned.


        rocket.move(1.0)


        rocket_status = rocket.get_status()  # Update the status of the rocket
        landed = rocket_status == lander_cpp.LanderStatus.LANDED # True/False variable that tells Python whether the rocket landed safely

        if (rocket_status == lander_cpp.LanderStatus.CRASHED):
            crashed = True
        else:
            crashed = False


        timed_out = counter >= 300 and rocket_status == lander_cpp.LanderStatus.FLYING # if counter is greater than or equal to 300 and the rocket is still flying, then it has timed out.
        new_fuel = rocket.get_fuel() # this is after the move because we need to compare fuel before and after movement to calculate how much was burned.

        step_reward = get_reward(landed, crashed, timed_out, fuel_before, new_fuel, 1.0)
        total_reward += step_reward


        new_altitude = rocket.get_altitude()
        new_velocity = rocket.get_velocity()

        print("AI throttle:", throttle)
        print("Altitude:", new_altitude)
        print("Velocity:", new_velocity)
        print("Fuel:", new_fuel)

        if new_altitude <= 0:
            print("Rocket has landed or crashed.")
            break

    print("Total Reward:", total_reward) # its after the loop because we want the final total reward after the rocket finishes flying.
