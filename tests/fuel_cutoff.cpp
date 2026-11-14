#include "../Lander.h"
#include <cassert>
#include <cmath>

int main() {
  Lander lander(10.0, 0.0, 1000.0, 1000.0, 0.5, 0.2, 1.0);
  assert(lander.move(1.0));
  assert(lander.getFuel() == 0.0);
  assert(lander.getThrottle() == 0.0);
  assert(std::abs(lander.getVelocity() - (-1.42)) < 1e-9);
  assert(std::abs(lander.getaltitude() - 8.9688) < 1e-9);
  assert(lander.move(1.0));
  assert(std::abs(lander.getVelocity() - (-3.04)) < 1e-9);
  assert(lander.getStatus() == FLYING);

  Lander safe(1.0, -1.0, 1000.0, 1000.0, 0.0, 0.0, 1.0);
  assert(safe.move(0.1));
  assert(safe.getStatus() == FLYING);
  while (safe.getStatus() == FLYING) assert(safe.move(0.1));
  assert(safe.getStatus() == LANDED);

  Lander fast(1.0, -10.0, 1000.0, 1000.0, 0.0, 0.0, 1.0);
  assert(fast.move(0.1));
  assert(fast.getStatus() == CRASHED);
}
