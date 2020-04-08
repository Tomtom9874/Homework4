
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
var Y{J} integer >= 0, <= 1;		
var x{I, J} integer >= 0, <= 1;
var D;
var s{J};
var budget;
var z integer >= 0, <= 1;


# Objective
minimize WorstDistance: D;

# Constraints
subject to DistrictDistance {i in I}: D >= sum{j in J} d[i,j] * x[i,j];
subject to DistrictAssigned{i in I}: sum{j in J} x[i,j] = 1;
subject to AssignedIsActive{j in J}: sum{i in I} x[i,j] <= Y[j] * card(I);
subject to ServicedPopulation{j in J}: s[j] = sum {i in I} p[i] * x[i,j];
subject to Budget: budget <= B;
subject to TrackBudget: budget = sum{j in J} (c[j] * s[j] + f[j] * Y[j]);
subject to CertainSites: Y[1] + Y[2] >= 2*z;
subject to CeratinSites2: Y[3] + Y[4] >= 2*(1-z);