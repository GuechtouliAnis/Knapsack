import streamlit as st
import Knap_funcs as kf

st.set_page_config("Knapsack",page_icon="icons/backpack.png",layout="wide")

y = ['Hammer','Screw','Towel','Wrench','Screwdriver']

kf.mixedInt(y)