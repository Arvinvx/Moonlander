# Lunar Moon Landing

A small C++ lunar lander simulation. The lander tracks altitude, velocity, throttle and fuel. When fuel runs out partway through a time step, it simulates the engine-on and engine-off portions separately.

Build with a C++17 compiler:

```sh
g++ -std=c++17 -Wall -Wextra -pedantic main.cpp Lander.cpp -o lander
./lander
```

Run the fuel-cutoff check:

```sh
g++ -std=c++17 -Wall -Wextra -pedantic tests/fuel_cutoff.cpp Lander.cpp -o fuel_cutoff
./fuel_cutoff
```

The original local folder remains unchanged. Compiled binaries are excluded from this repository.
