import os
import shutil
import urbs


input_files = 'Bosnia2030_withoutCo2limit_PV150_CO2pricelowPVWindlimit.xlsx'  # for single year file name, for intertemporal folder name
input_dir = 'Input'
input_path = os.path.join(input_dir, input_files)

result_name = 'Bosnia2030_withoutCo2limit_PV150_CO2pricelowPVWindlimit'
result_dir = urbs.prepare_result_directory(result_name)  # name + time stamp

# copy input file to result directory
try:
    shutil.copytree(input_path, os.path.join(result_dir, input_dir))
except NotADirectoryError:
    shutil.copyfile(input_path, os.path.join(result_dir, input_files))
# copy run file to result directory
shutil.copy(__file__, result_dir)

# objective function
objective = 'cost'  # set either 'cost' or 'CO2' as objective

# Choose Solver (cplex, glpk, gurobi, ...)
solver = 'gurobi'

# simulation timesteps
(offset, length) = (0, 8759)  #8760 # time step selection
timesteps = range(offset, offset+length+1)
dt = 1  # length of each time step (unit: hours)

# detailed reporting commodity/sites
report_tuples = [
    #(2020, 'CA', 'ElecGrid'), 
    (2030, 'FederationBiH', 'Elec'),    
    (2030, 'Republika Srpska', 'Elec'),
    (2030, ['FederationBiH','Republika Srpska'], 'Elec'),
    (2030, 'FederationBiH', 'CO2'),    
    (2030, 'Republika Srpska', 'CO2'),
    ]

# optional: define names for sites in report_tuples
report_sites_name = {('FederationBiH', 'Republika Srpska'): 'All'}

# plotting commodities/sites
plot_tuples = [
    #(2030, 'FederationBiH', 'Elec'),    
    #(2030, 'Republika Srpska', 'Elec'),
    ]

# optional: define names for sites in plot_tuples
plot_sites_name = {}

# plotting timesteps
plot_periods = {
    'all': timesteps[1:],
    #'summer_week':timesteps[4000:4168],
}

# add or change plot colors
my_colors = {
    'FederationBiH': (230, 200, 200),
    'Republika Srpska': (230, 200, 200)}
for country, color in my_colors.items():
    urbs.COLORS[country] = color

# select scenarios to be run
scenarios = [
             urbs.scenario_base,

            ]

for scenario in scenarios:
    prob = urbs.run_scenario(input_path, solver, timesteps, scenario,
                             result_dir, dt, objective,
                             plot_tuples=plot_tuples,
                             plot_sites_name=plot_sites_name,
                             plot_periods=plot_periods,
                             report_tuples=report_tuples,
                             report_sites_name=report_sites_name)
