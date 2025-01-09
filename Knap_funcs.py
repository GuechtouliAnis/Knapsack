import streamlit as st
import pandas as pd
import numpy as np
from gekko import GEKKO

def get_values(values,min_value=0,max_value=40):
    """
    Prompts the user to input the values of five items (Hammer, Screw, Towel, Wrench, Screwdriver)
    using Streamlit's number_input widget. The values are added to the provided list 'values'
    and returned after user input.

    Parameters:
    values (list): A list to store the user-inputted values for each item.

    Returns:
    list: The updated list containing the user-provided values for the five items.
    """
    
    # Get the value for the Hammer and append it to the values list
    values.append(st.number_input("Hammer Value", min_value=min_value, max_value=max_value, value=7))

    # Get the value for the Screw and append it to the values list
    values.append(st.number_input("Screw Value", min_value=min_value, max_value=max_value, value=5))

    # Get the value for the Towel and append it to the values list
    values.append(st.number_input("Towel Value", min_value=min_value, max_value=max_value, value=8))

    # Get the value for the Wrench and append it to the values list
    values.append(st.number_input("Wrench Value", min_value=min_value, max_value=max_value, value=3))

    # Get the value for the Screwdriver and append it to the values list
    values.append(st.number_input("Screwdriver Value", min_value=min_value, max_value=max_value, value=6))

    # Return the updated list of values
    return values

def get_weights(weights, min_value=0, max_value=100):
    """
    Prompts the user to input the weights of five items (Hammer, Screw, Towel, Wrench, Screwdriver)
    using Streamlit's number_input widget. The weights are added to the provided list 'weights'
    and returned after user input.

    Parameters:
    weights (list): A list to store the user-inputted weights for each item.
    min_value (int, optional): The minimum weight value. Defaults to 0.
    max_value (int, optional): The maximum weight value. Defaults to 100.

    Returns:
    list: The updated list containing the user-provided weights for the five items.
    """
    
    # Get the weight for the Hammer and append it to the weights list
    weights.append(st.number_input("Hammer Weight", min_value=min_value, max_value=max_value, value=3))

    # Get the weight for the Screw and append it to the weights list
    weights.append(st.number_input("Screw Weight", min_value=min_value, max_value=max_value, value=2))

    # Get the weight for the Towel and append it to the weights list
    weights.append(st.number_input("Towel Weight", min_value=min_value, max_value=max_value, value=5))

    # Get the weight for the Wrench and append it to the weights list
    weights.append(st.number_input("Wrench Weight", min_value=min_value, max_value=max_value, value=7))

    # Get the weight for the Screwdriver and append it to the weights list
    weights.append(st.number_input("Screwdriver Weight", min_value=min_value, max_value=max_value, value=4))

    # Return the updated list of weights
    return weights

def mix_int(v, w, y, limit, o):
    """
    Solves a mixed-integer optimization problem to determine the optimal selection of items 
    to include in a knapsack based on their values and weights. The optimization is performed 
    using the GEKKO solver, maximizing the total value without exceeding a weight limit.

    Parameters:
    v (list): List of values corresponding to the items.
    w (list): List of weights corresponding to the items.
    y (list): List of item names.
    limit (int): The maximum allowable weight for the knapsack.
    o (int): Upper bound for the number of items to include (e.g., 1 for 0/1 knapsack, 100 for unbound).

    Returns:
    pd.DataFrame: A DataFrame containing the solution with item quantities, total value, and total weight.
    """
    
    # Determine the number of items
    items = len(y)
    
    # Create a GEKKO optimization model
    m = GEKKO(remote=False)

    # Create an array of variables representing the number of each item to include in the knapsack
    x = m.Array(m.Var, len(y), lb=0, ub=o, integer=True)
    
    # Set up the objective function to maximize the total value of items in the knapsack
    m.Maximize(m.sum([v[i] * x[i] for i in range(items)]))
    
    # Add constraint to ensure the total weight of items in the knapsack doesn't exceed the limit
    m.Equation(m.sum([w[i] * x[i] for i in range(items)]) <= limit)

    # Choose the solver & solve the optimization problem
    m.options.SOLVER = 1
    m.solve()

    # Calculate the total weight of items in the knapsack
    tw = sum([w[i] * x[i].value[0] for i in range(items)])

    # Create a dictionary to store the solution (quantities of each item selected)
    data = {item: [x[i].value[0]] for i, item in enumerate(y)}
    
    # Create a DataFrame to display the solution
    df = pd.DataFrame(data)
    
    # Add columns for the total value and total weight of items in the knapsack
    df["Value"] = int((-m.options.objfcnval))  # Total value is the negative of the objective function value
    df["Weight"] = sum([w[i] * x[i].value[0] for i in range(items)])  # Total weight of selected items
    
    # Increment the index of the DataFrame by 1 for user-friendly display
    df.index += 1
    
    # Return the DataFrame containing the solution
    return df

def get_state(item, df):
    """
    Determines the state of an item based on its value in the provided DataFrame.
    If the value of the item is greater than 0, it returns an "on" state with a green color; 
    otherwise, it returns an "off" state with a gray color.

    Parameters:
    item (str): The name of the item to check the state for.
    df (pd.DataFrame): A DataFrame containing the item values.

    Returns:
    list: A list containing the state ("on" or "off") and corresponding color code.
    """
    # Return the state and color based on the value of the item in the DataFrame
    return ["on", "#00ff00"] if df.iloc[0][item] > 0 else ["off", "#aaa"]

def visualize(df):
    """
    Visualizes the state of each item in the knapsack (Hammer, Screw, Towel, Wrench, Screwdriver)
    by displaying images representing their "on" or "off" states based on the corresponding
    values in the provided DataFrame. Also, it displays the item names and the quantities in the
    selected color.

    Parameters:
    df (pd.DataFrame): A DataFrame containing the quantities of each item in the knapsack.
    """
    
    # List of item names to visualize
    items = ['Hammer', 'Screw', 'Towel', 'Wrench', 'Screwdriver']
    
    # Create a dictionary with the state images for each item (on/off states)
    state_images = {item: f"icons/{get_state(item, df)[0]}_{item}.png" for item in items}
    
    # Create columns for displaying each item
    columns = st.columns([1, 1, 1, 1, 1])

    # Iterate over the items and corresponding columns to display them
    for item, col in zip(items, columns):
        # Get the state (on/off) and color for the item
        state = get_state(item, df)
        
        # Display the image representing the item's state (on/off)
        col.image(state_images[item], caption=str(item), use_column_width=True)
        
        # Display the item's quantity with the corresponding color
        col.caption(f"""<div style="text-align:center">
                    <H1 style="color:{state[1]};">{int(df.iloc[0][item])}</H1></div>""",
                    unsafe_allow_html=True)

def mixedInt(y):
    """
    Solves a knapsack optimization problem by allowing the user to input values and weights for items 
    and select the knapsack type (0/1 or unbound). It then calls the `mix_int` function to solve the 
    optimization problem and visualizes the results.

    Parameters:
    y (list): List of item names used for knapsack items.

    Returns:
    None
    """
    
    # Initialize empty lists for weights and values
    weights = []
    values = []

    # Create two columns for layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    # In the first column, set up the form to get values and knapsack size limit
    with col1.container(height=620, border=True).form("zero_one", border=False):
        c1, c2 = st.columns([1, 1])
        
        # In the first sub-column, get values for items and set knapsack size limit
        with c1:
            values = get_values(values)
            limit = st.number_input("Enter sack size", min_value=1, max_value=100, value=15)

        # In the second sub-column, get weights for items and select knapsack type
        with c2:
            weights = get_weights(weights)
            kt = st.radio("Select knapsack type",
                ["0/1", "Unbound"], horizontal=True)

        # Display a caption guiding the user to submit the form for calculation
        st.caption("""<div style="text-align:center">
                    <p>Click submit to calculate the best case</p></div>""", unsafe_allow_html=True)

        # Create submit button for the form
        co1, co2, co3 = st.columns([1.5, 1, 1.5])
        zo_submit = co2.form_submit_button("submit", use_container_width=True)

    # Ensure that zero weights correspond to zero values and vice versa
    for i in range(len(weights)):
        if weights[i] == 0: 
            values[i] = 0
        if values[i] == 0: 
            weights[i] = 0

    # In the second column, solve the optimization problem and visualize the result
    with col2.container(height=620):
        # Determine if knapsack type is 0/1 or unbound
        o = 1 if kt == "0/1" else 100
        
        # Call the mix_int function to solve the optimization problem
        df = mix_int(values, weights, y, limit, o)

        # Visualize the result
        visualize(df)
        
        # Display the DataFrame with the solution
        st.dataframe(df, use_container_width=True)

        # Check if there are any invalid weights or values
        arr = np.array(weights)
        err = ((arr >= 1) & (arr <= limit)).any()
        
        # If there are invalid values, display a warning
        if not err:
            st.warning("Invalid weights or values.")