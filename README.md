Installing requirements:
After installing the requirements by running "pip install -r Optimisation/requirements.txt"
in your command shell, you have to start the app using "streamlit run Optimisation/Knap.py".

To run:
Of if you're inside "Optimisation" directory:
- "pip install -r requirements.txt"
- "streamlit run Knap.py"

Optimisation/used folder contains:
- The pure knapsack algorithm made with gekko in "knapsack.py"
which is a python script that can be run in the shell/terminal.
- Our hard-coded solution for the Knapsack problem in "Interface.py"
which is a streamlit interface that solves the knapsack problem but can take
a long time to execute as it considers all the possible solutions.

- "Optimisation/used/Int_funcs.py" and "Optimisation/Knap_funcs.py" are the functions called by the two main
codes in "Optimisation/used/Interface.py" and "Optimisation/Knap.py" respectively.

- "Optimisation/icons" contains the icons and images used by the visualisations