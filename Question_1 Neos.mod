reset;

# Sets
set I; # Districts
set J; # Postential Sites

# Parameters
param p{I} >= 0; # Population in each district
param d{I,J} >= 0; # Distance in km from district to site
param B >= 0; # Budget
param f{J} >= 0; # Fixed cost of the site
param c{J} >= 0; # Variable cost associated with the site

# Variables
var Y{I} integer >= 0, <= 1;
var X{I, J} integer >= 0, <= 1;
var D;
var s{J};

# Objective
minimize WorstDistance: D;

# Constraints
subject to DistrictDistance {i in I}: D >= sum{j in J} d[i,j] * X[i,j];
subject to DistrictAssigned{i in I}: sum{j in J} X[i,j] = 1;
subject to AssignedIsActive{j in J}: sum{i in I} X[i,j] <= Y[j] * card(I);
subject to ServicedPopulation{j in J}: s[j] = sum {i in I} p[i] * X[i,j];
subject to Budget:sum{j in J} (c[j] * s[j] + f[j] * Y[j]) <= B;

data firehouse-d2mini.dat;
solve;
display WorstDistance;
display Y;
display X;