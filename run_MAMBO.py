# Importing modules
import os
import sys
import numpy
import cobra
import cplex
import gurobipy
import csv
import pandas as pd
import bottom_up_ecology as bte


# Code to read in command-line arguments positionally and throw
# error/help message if incorrect number of arguments.
if len(sys.argv) != 5:
    sys.exit("Stopping - expected five positional arguments:"
            "(1) input abundance table, (2) table of sorted models delimited by new-line breaks, "
            "(3) path to folder containing models, (4) the output file,"
            "and (5) the number of desired MCMC runs.")
else:
    abundance_file = sys.argv[1]
    model_list = sys.argv[2]
    model_directory = sys.argv[3]
    output_file = sys.argv[4]
    runs = sys.argv[5]


# Load abundance file
abundance = numpy.genfromtxt(abundance_file)


# Convert to relative abundances
relative_abundance = numpy.divide(abundance, abundance.sum())


# Identifying model indices that correspond to non-zero abundance values
models2keep = numpy.asarray(numpy.where(relative_abundance > 0))[0]


# Remove zero-value abundances
relative_abundance = relative_abundance[relative_abundance != 0]


# Read in file names and append folder name to start of string
with open(model_list, 'r') as f:
  model_files = [line.strip() for line in f]


# Read in cobra models in specified sorted order
models = [cobra.io.read_sbml_model(model_directory + '/' + (model_files)[i])
          for i in models2keep]


# Initializing MAMBO environment
evolution_of_exchange_reactions = {}
initial_environment = bte.starting_environment(models)
metabs = initial_environment.keys()


# Setting solver
for i in range(len(models)):
    models[i].solver = 'gurobi'


# Running MAMBO
for i in xrange(runs):
  print(i)
  bte.single_MCMC_run(numpy.random.random_integers(0, len(metabs) - 1), models, initial_environment, metabs, relative_abundance, evolution_of_exchange_reactions , i)


# Retrieving keys for top ten percent of predictions
top = sorted(evolution_of_exchange_reactions.keys(), key = lambda x: x[1], reverse = True)[0:(len(evolution_of_exchange_reactions) / 10)]


# Subsetting predictions to extract only top performing predictions
top_pred = {key:evolution_of_exchange_reactions[key] for key in top}


# Changing tuple key to first element representing run number and
# moving second element (Pearson correlation) to values
pred = dict()
for key,value in top_pred.items():
    new_val = value
    new_val.update({"pearson_correlation": key[1]})
    pred[key[0]] = new_val


# Creating dataframe and removing preffixes/suffixes from SEED compound IDs
pred_data = pd.DataFrame(pred)
pred_data.index = pred_data.index.str.replace("^EX_|_e0$", "")


# Exporting to .csv
pred_data.to_csv(output_file, index = True, header = True)
