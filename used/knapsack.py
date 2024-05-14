from gekko import GEKKO

y = ['hammer','screw','towel','wrench','screwdriver']
w = [1,1,1,1,1]
v = [5,0,5,5,5]
items = len(y)

# Create model
m = GEKKO()

# Variables
x = m.Array(m.Var,len(y),lb=0,ub=10,integer=True)

# Objective
m.Maximize(m.sum([v[i]*x[i] for i in range(items)]))

# Constraint
limit = 15
m.Equation(m.sum([w[i]*x[i] for i in range(items)]) <= limit)

# Optimize with APOPT
m.options.SOLVER = 1

m.solve()

# Print the value of the variables at the optimum
for i in range(items):
    print("%s = %f" % (y[i], x[i].value[0]))

# Print the value of the objective
print("Objective = %f" % (-m.options.objfcnval))
total_weight = sum([w[i]*x[i].value[0] for i in range(items)])
print("Total Weight = %f" % total_weight)
print("\nX")
print(x)
print("\nY")
print(y)