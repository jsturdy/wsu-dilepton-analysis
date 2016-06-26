#ifndef COSMIC_BIN_FUNCTIONS
#define COSMIC_BIN_FUNCTIONS

int getChargeBin(double chargeval) {
  // returns bin 0 for positive charge, 1 for negative charge
  return chargeval > 0 ? 1 : 0;
}

int getEtaBin(double etaval) {
  // returns bin 0 for positive eta, 1 for negative eta
  return etaval > 0 ? 1 : 0;
}

int getPhiBin(double phival) {
  // returns bin 0 for phi > pi/3, 1 for -pi/3 < phi < pi/3, 2 for phi < -pi/3
  return phival > M_PI/3. ? 0 : (phival > -M_PI/3. ? 1 : 2);
}

#endif
