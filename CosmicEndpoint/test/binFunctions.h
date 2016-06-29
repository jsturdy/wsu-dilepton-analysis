#ifndef COSMIC_BIN_FUNCTIONS
#define COSMIC_BIN_FUNCTIONS

int getChargeBin(double chargeval) {
  // returns bin 0 for negative charge, 1 for positive charge
  return chargeval < 0 ? 0 : 1;
}

int getEtaBin(double etaval) {
  // returns bin 0 for negative eta, 1 for positive eta
  return etaval < 0 ? 0 : 1;
}

int getPhiBin(double phival) {
  // returns bin 0 for phi < -pi/3, 1 for -pi/3 < phi < pi/3, 2 for phi > pi/3
  return phival < -M_PI/3. ? 0 : (phival < M_PI/3. ? 1 : 2);
}

#endif
