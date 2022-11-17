# MAMBO_MCMC_run
Script to run the MAMBO tool as described by [Garza et al. (2018)](https://www.nature.com/articles/s41564-018-0124-8). The algorithm optimizes correlations between relative microbial growth rates (as estimated using constraint-based modelling) and microbial abundances obtained through sequencing. Requires the [original MAMBO repo](https://github.com/danielriosgarza/MAMBO) and all associated dependencies.

This script is designed to be run in parallel using GNU Parallel and requires several inputs:

* newline-delimited `.txt` file containing microbial abundances within a single sample (several examples in `/mambo_in`)
* newline-delimted `.txt` file containing a list of all the genome-scale metabolic (GEM) models associated with the sample microbial abundances (e.g., `model_list.txt`). Refer to [this](https://github.com/danielriosgarza/bacterial_passengers.py/blob/master/input_for_ipython_scripts/bac_database.tsv) file to match the taxa in your samples to those represented by the GEM models.
* genome-scale metabolic models obtained from the MAMBO repo (I have included all the ones necessary to run the examples)

The script will run the user-defined number of Marko chain Monte Carlo (MCMC) runs, filter out predictions to retain only the predictions within the top ten percent (as measured using the tool's internal Pearson correlation output), and output a `.csv` file containing the reaction predictions. 

## Example of usage
```
parallel -j JOBS --eta 'python run_MAMBO.py {} model_list.txt models mambo_out/{/.}.csv RUNS' ::: mambo_in/*txt
```
```
JOBS  Number of parallel jobs to run
RUNS  Number of Markov chain Monte Carlo runs per sample (tool author recommends 1,000,000) 
```
