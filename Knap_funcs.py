import streamlit as st
import pandas as pd
import numpy as np
from gekko import GEKKO

def get_values(values):
    values.append(st.number_input("Hammer Value",min_value=0,max_value=40,value=7))
    values.append(st.number_input("Screw Value",min_value=0,max_value=40,value=5))
    values.append(st.number_input("Towel Value",min_value=0,max_value=40,value=8))
    values.append(st.number_input("Wrench Value",min_value=0,max_value=40,value=3))
    values.append(st.number_input("Screwdriver Value",min_value=0,max_value=40,value=6))
    return values

def get_weights(weights):
    weights.append(st.number_input("Hammer Weight",min_value=0,max_value=100,value=3))
    weights.append(st.number_input("Screw Weight",min_value=0,max_value=100,value=2))
    weights.append(st.number_input("Towel Weight",min_value=0,max_value=100,value=5))
    weights.append(st.number_input("Wrench Weight",min_value=0,max_value=100,value=7))
    weights.append(st.number_input("Screwdriver Weight",min_value=0,max_value=100,value=4))
    return weights

def mix_int(v,w,y, limit,o):
    # Determine the number of items
    items = len(y)
    
    # Create a GEKKO optimization model
    m=GEKKO(remote=False)

    # Create an array of variables representing the number of each item to include in the knapsack
    x = m.Array(m.Var,len(y),lb=0,ub=o,integer=True)
    
    # Set up the objective function to maximize the total value of items in the knapsack
    m.Maximize(m.sum([v[i]*x[i] for i in range(items)]))
    # Add constraint to ensure the total weight of items in the knapsack doesn't exceed the limit
    m.Equation(m.sum([w[i]*x[i] for i in range(items)]) <= limit)

    # Choose the solver & solve the optimization problem
    m.options.SOLVER = 1
    m.solve()

    # Calculate the total weight of items in the knapsack
    tw = sum([w[i]*x[i].value[0] for i in range(items)])

    # Create a dictionary to store the solution
    data = {item: [x[i].value[0]] for i, item in enumerate(y)}
    # Create a DataFrame to display the solution
    df = pd.DataFrame(data)
    # Add columns for the total value and total weight of items in the knapsack
    df["Value"] = int((-m.options.objfcnval))
    df["Weight"] = sum([w[i]*x[i].value[0] for i in range(items)])
    # Increment the index of the DataFrame by 1
    df.index += 1
    # Return the DataFrame containing the solution
    return df

def get_state(item,df):
    return ["on", "#00ff00"] if df.iloc[0][item] > 0 else ["off", "#aaa"]

def visualize(df):

    items = ['Hammer', 'Screw', 'Towel', 'Wrench', 'Screwdriver']
    state_images = {item: f"icons/{get_state(item,df)[0]}_{item}.png" for item in items}
    columns = st.columns([1, 1, 1, 1, 1])

    for item, col in zip(items, columns):
        state = get_state(item,df)
        col.image(state_images[item],caption=str(item),use_column_width=True)
        col.caption(f"""<div style="text-align:center">
                    <H1 style="color:{state[1]};">{int(df.iloc[0][item])}</H1></div>""",
                    unsafe_allow_html=True)

def mixedInt(y):
    # Initialize empty lists for weights and values
    weights = []
    values = []
    col1, col2 = st.columns([1,1],gap="large")
    with col1.container(height=620,border=True).form("zero_one",border=False):
        c1,c2=st.columns([1,1])
        with c1:
            # First sub-column: get values for items and set knapsack size limit
            values = get_values(values)
            limit = st.number_input("Enter sack size",min_value=1,max_value=100,value=15)

        with c2:
            # Second sub-column: get weights for items and select knapsack type
            weights = get_weights(weights)
            kt = st.radio("Select knapsack type",
                ["0/1", "Unbound"],horizontal=True)

        st.caption("""<div style="text-align:center">
                    <p>Click submit to calculate the best case</p></div>""", unsafe_allow_html=True)

        co1,co2,co3 = st.columns([1.5,1,1.5])
        zo_submit = co2.form_submit_button("submit",use_container_width=True)

    # Ensure that zero weights correspond to zero values and vice versa
    for i in range(len(weights)):
        if weights[i] == 0: values[i]  = 0
        if values[i]  == 0: weights[i] = 0

    with col2.container(height=620):

        # Determine if knapsack type is 0/1 or unbound
        o = 1 if kt =="0/1" else 100
        # Solve the mixed-integer optimization problem
        df = mix_int(values,weights,y,limit,o)

        visualize(df)
        st.dataframe(df,use_container_width=True)

        # Check for invalid weights or values
        arr = np.array(weights)
        err = ((arr >= 1) & (arr <= limit)).any()
        
        if not err:
            st.warning("Invalid weights or values.")