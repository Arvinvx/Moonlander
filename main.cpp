#include "Lander.h"
#include <iostream>

int main(){
    Lander rocket(1000, -50, 1000, 3000, 0.2, 0.8, 2);
    int counter = 0;

    while (rocket.getaltitude() > 0) {

        if (rocket.move(1.0) == true) {
