import pandas as pd
from pyomo.environ import ConcreteModel, Set, Var, Objective, Constraint, maximize, SolverFactory, NonNegativeReals, Binary

# Read data from Excel
df = pd.read_excel('CES_GridBOOST_Problem_Statement_Data.xlsx')
hours = df['HOURs'].values
prices = df['DAM_PRICE ($/MWh)'].values

# Model
model = ConcreteModel()

# Sets
model.T = Set(initialize=range(len(hours)), ordered=True)

# Parameters
max_power = 10  # MW
max_soc = 40  # MWh
min_soc = 0.05 * max_soc  # MWh
charge_efficiency = 0.9
discharge_efficiency = 1.0
deg_cost = 10  # $/MWh
total_discharge_limit = 14600  # MWh

# Variables
model.C = Var(model.T, within=NonNegativeReals, bounds=(0, max_power))  # Charging power in MW
model.D = Var(model.T, within=NonNegativeReals, bounds=(0, max_power))  # Discharging power in MW
model.SoC = Var(model.T, within=NonNegativeReals, bounds=(min_soc, max_soc))  # State of Charge in MWh
model.Y = Var(model.T, within=Binary)  # 1 if charging, 0 if discharging

# Objective
model.obj = Objective(expr=sum(prices[t] * model.D[t] * discharge_efficiency - prices[t] * model.C[t] / charge_efficiency - deg_cost * model.D[t] for t in model.T), sense=maximize)

# Constraints
def storage_balance_rule(model, t):
    if t == model.T.first():
        return model.SoC[t] == min_soc
    return model.SoC[t] == model.SoC[t-1] + charge_efficiency * model.C[t] - model.D[t]

model.storage_balance = Constraint(model.T, rule=storage_balance_rule)
model.charge_constraint = Constraint(model.T, rule=lambda model, t: model.C[t] <= max_power * model.Y[t])
model.discharge_constraint = Constraint(model.T, rule=lambda model, t: model.D[t] <= max_power * (1 - model.Y[t]))
def total_discharge_rule(model):
    return sum(model.D[t] for t in model.T) <= total_discharge_limit

model.total_discharge = Constraint(rule=total_discharge_rule)

# Solve
solver = SolverFactory('glpk')
results = solver.solve(model, tee=True)

# Extract results to lists
charging_mwh = [model.C[t].value for t in model.T]
discharging_mwh = [model.D[t].value for t in model.T]
soc = [model.SoC[t].value for t in model.T]
hourly_revenue = [prices[t] * model.D[t].value * discharge_efficiency - prices[t] * model.C[t].value / charge_efficiency - deg_cost * model.D[t].value for t in model.T]

# Write to Excel
output_df = pd.DataFrame({
    'Hour': hours,
    'Charging (MWh)': charging_mwh,
    'Discharging (MWh)': discharging_mwh,
    'State of Charge (MWh)': soc,
    'Hourly Revenue from DAM market ($)': hourly_revenue
})

output_df.to_excel('output_results.xlsx', index=False)
