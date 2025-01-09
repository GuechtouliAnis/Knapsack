import streamlit as st
import Knap_funcs as kf

def main():
    """
    Main function to run the Knapsack problem application.

    This script configures the Streamlit app, defines the items for the knapsack problem,
    and then calls the `mixedInt` function from the `Knap_funcs` module to solve the 
    knapsack optimization problem and visualize the results.

    Flow:
    1. Configures Streamlit page layout and title.
    2. Defines a list of items to include in the knapsack.
    3. Calls `kf.mixedInt()` to process the knapsack problem.
    """
    
    # Set the page configuration for Streamlit
    st.set_page_config("Knapsack", page_icon="icons/backpack.png", layout="wide")

    # List of items to include in the knapsack problem
    y = ['Hammer', 'Screw', 'Towel', 'Wrench', 'Screwdriver']

    # Call the `mixedInt` function from Knap_funcs to solve the knapsack problem
    kf.mixedInt(y)

# Ensure the script runs only if it is executed directly
if __name__ == "__main__":
    main()
