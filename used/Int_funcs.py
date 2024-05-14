import streamlit as st
import pandas as pd
import numpy as np
from itertools import product

#Done
def get_values(values):
    values.append(st.number_input("Hammer Value",min_value=0,max_value=40,value=7))
    values.append(st.number_input("Screw Value",min_value=0,max_value=40,value=5))
    values.append(st.number_input("Towel Value",min_value=0,max_value=40,value=8))
    values.append(st.number_input("Wrench Value",min_value=0,max_value=40,value=3))
    values.append(st.number_input("Screwdriver Value",min_value=0,max_value=40,value=6))
    return values

#Done
def get_weights(weights):
    weights.append(st.number_input("Hammer Weight",min_value=0,max_value=100,value=3))
    weights.append(st.number_input("Screw Weight",min_value=0,max_value=100,value=2))
    weights.append(st.number_input("Towel Weight",min_value=0,max_value=100,value=5))
    weights.append(st.number_input("Wrench Weight",min_value=0,max_value=100,value=7))
    weights.append(st.number_input("Screwdriver Weight",min_value=0,max_value=100,value=4))
    return weights

def removing (weights,values,kd,sack_size):
    toremove = []
    for j in range(len(weights)):
        if weights[j] == 0 or values[j] == 0 or weights[j]>sack_size:
            toremove.append(j)

    hea = 5
    if len(toremove) <5:
        p = 0
        for s in toremove:
            weights.pop(s-p)
            values.pop(s-p)
            kd['Tools'].pop(s-p)
            p +=1
    else:
        hea = 1
    kd["weights"] = weights
    kd["values"] = values
    kd = pd.DataFrame(kd,index=kd['Tools'])
    kd.drop('Tools', axis=1, inplace=True)
    return kd.transpose(), hea

def check_weights(weights, sack_size):
    for weight in weights:
        if 1 <= weight <= sack_size:
            return True
    return False

def gen_cases(size):
    cases = []
    for i in range(size):
        binary_string = bin(i)
        binary_string_without_prefix = binary_string[2:]
        cases.append(binary_string_without_prefix)
    for pos in range(len(cases)):
        length = len(cases[-1]) - len(cases[pos])
        if length !=0:
            for i in range(length):
                cases[pos] = "0"+cases[pos]
        else:
            break
    return cases

def zo(df_01,sack_size):
    size = 2 ** len(df_01.columns)
    cases = gen_cases(size)
    cpt = 1
    for poss in cases:
        f = []
        for n in poss:
            f.append(int(n))
            s = str(cpt)
        df_01.loc["pos"+s]=f
        cpt +=1
    sums = [df_01.loc['values'].sum(),df_01.loc['weights'].sum()]
    weight = [df_01.loc['values'].sum(),df_01.loc['weights'].sum()]
    for i in range(1,len(df_01)-1):
        s = 0
        w = 0
        for col in df_01.columns:
            s += df_01.loc['pos'+str(i),col] * df_01.loc['values',col]
            w += df_01.loc['pos'+str(i),col] * df_01.loc['weights',col]
        sums.append(s)
        weight.append(w)
    df_01['Total Values'] = sums
    df_01['Total Weights'] = weight
    dfs_01 = df_01.drop(["values","weights"])
    dfs_01 = dfs_01[dfs_01["Total Weights"]<= sack_size]
    order = ["Total Values","Total Weights"]
    asc = [False,True]
    dfs_01=dfs_01.sort_values(by=order,ascending=asc)
    dfs_01.reset_index(drop=True, inplace=True)

    # Adding 1 to index to start from 1 instead of 0
    dfs_01.index += 1
    return dfs_01

def unb(df_02,sack_size):
    li = []
    for i in df_02.columns:
        mod = 15 / df_02.loc["weights", i]
        r = range(int(mod)+1)
        li.append(list(r))
    combinations = product(*li)
    filtered_combinations = []
    for combo in combinations:
        valid = True
        for i, val in enumerate(combo):
            if sum(val * df_02.loc["weights", df_02.columns[i]] for i, val in enumerate(combo)) >= 1000:
                valid = False
                break
        if valid:
            filtered_combinations.append(combo)
    df_unb = df_02.copy()
    cpt = 1
    for comb in filtered_combinations:
        df_unb.loc["pos"+str(cpt)] = comb
        cpt += 1
    sums = [df_unb.loc['values'].sum(),df_unb.loc['weights'].sum()]
    weights = [df_unb.loc['values'].sum(),df_unb.loc['weights'].sum()]
    for i in range(1,len(df_unb)-1):
        s = 0
        w = 0
        for col in df_unb.columns:
            s += df_unb.loc['pos'+str(i),col] * df_unb.loc['values',col]
            w += df_unb.loc['pos'+str(i),col] * df_unb.loc['weights',col]
        sums.append(s)
        weights.append(w)
    df_unb['Total Values'] = sums
    df_unb['Total Weights'] = weights
    df_unb = df_unb.drop(["values","weights"])
    dfs_unb = df_unb[df_unb["Total Weights"]<= sack_size]
    dfs_unb = dfs_unb.sort_values(by=["Total Values","Total Weights"],ascending=[False,True])

    dfs_unb.reset_index(drop=True, inplace=True)

    # Adding 1 to index to start from 1 instead of 0
    dfs_unb.index += 1

    return dfs_unb

def visuals(dfs_01):
    im1,im2,im3,im4,im5=st.columns([1,1,1,1,1])
    im1.caption(f"""<div style="text-align:center"><p>Hammer</p></div>""", unsafe_allow_html=True)
    if "Hammer" in dfs_01:
        if dfs_01.iloc[0]["Hammer"]>0:
            im1.image("icons/on_Hammer.png")
            im1.caption(f"""<div style="text-align:center"><H1 style="color:#00ff00;">{dfs_01.iloc[0]["Hammer"]}</H1></div>""", unsafe_allow_html=True)
        else:
            im1.image("icons/off_Hammer.png")
            im1.caption(f"""<div style="text-align:center"><H1>{dfs_01.iloc[0]["Hammer"]}</H1></div>""", unsafe_allow_html=True)
    else:
        im1.image("icons/off_Hammer.png")
        im1.caption(f"""<div style="text-align:center"><H1>0</H1></div>""", unsafe_allow_html=True)
    im2.caption(f"""<div style="text-align:center"><p>Screw</p></div>""", unsafe_allow_html=True)
    if "Screw" in dfs_01:
        if dfs_01.iloc[0]["Screw"]>0:
            im2.image("icons/on_Screw.png")
            im2.caption(f"""<div style="text-align:center">
            <H1 style="color:#00ff00;">{dfs_01.iloc[0]["Screw"]}</H1></div>""", unsafe_allow_html=True)
        else:
            im2.image("icons/off_Screw.png")
            im2.caption(f"""<div style="text-align:center"><H1>{dfs_01.iloc[0]["Screw"]}</H1></div>""", unsafe_allow_html=True)
    else:
        im2.image("icons/off_Screw.png")
        im2.caption(f"""<div style="text-align:center"><H1>0</H1></div>""", unsafe_allow_html=True)
    im3.caption(f"""<div style="text-align:center"><p>Towel</p></div>""", unsafe_allow_html=True)
    if "Towel" in dfs_01:
        if dfs_01.iloc[0]["Towel"]>0:
            im3.image("icons/on_Towel.png")
            im3.caption(f"""<div style="text-align:center"><H1 style="color:#00ff00;">{dfs_01.iloc[0]["Towel"]}</H1></div>""", unsafe_allow_html=True)
        else:
            im3.image("Optimisation/icons/off_Towel.png")
            im3.caption(f"""<div style="text-align:center"><H1>{dfs_01.iloc[0]["Towel"]}</H1></div>""", unsafe_allow_html=True)    
    else:
        im3.image("icons/off_Towel.png")
        im3.caption(f"""<div style="text-align:center"><H1>0</H1></div>""", unsafe_allow_html=True)
    im4.caption(f"""<div style="text-align:center"><p>Wrench</p></div>""", unsafe_allow_html=True)
    if "Wrench" in dfs_01:
        if dfs_01.iloc[0]["Wrench"]>0:
            im4.image("icons/on_Wrench.png")
            im4.caption(f"""<div style="text-align:center"><H1 style="color:#00ff00;">{dfs_01.iloc[0]["Wrench"]}</H1></div>""", unsafe_allow_html=True)
        else:
            im4.image("icons/off_Wrench.png")
            im4.caption(f"""<div style="text-align:center"><H1>{dfs_01.iloc[0]["Wrench"]}</H1></div>""", unsafe_allow_html=True)
    else:
        im4.image("icons/off_Wrench.png")
        im4.caption(f"""<div style="text-align:center"><H1>0</H1></div>""", unsafe_allow_html=True)
    im5.caption(f"""<div style="text-align:center"><p>Screwdriver</p></div>""", unsafe_allow_html=True)
    if "Screwdriver" in dfs_01:
        if dfs_01.iloc[0]["Screwdriver"]>0:
            im5.image("icons/on_Screwdriver.png")
            im5.caption(f"""<div style="text-align:center"><H1 style="color:#00ff00;">{dfs_01.iloc[0]["Screwdriver"]}</H1></div>""", unsafe_allow_html=True)
        else:
            im5.image("icons/off_Screwdriver.png")
            im5.caption(f"""<div style="text-align:center"><H1>{dfs_01.iloc[0]["Screwdriver"]}</H1></div>""", unsafe_allow_html=True)
    else:
            im5.image("icons/off_Screwdriver.png")
            im5.caption(f"""<div style="text-align:center"><H1>0</H1></div>""", unsafe_allow_html=True)

#Done
def zero_one_knap(kd):
    weights = []
    values = []
    zo_col1, zo_col2 = st.columns([1,1],gap="large")
    with zo_col1.container(height=620,border=True).form("zero_one",border=False):
        c1,c2=st.columns([1,1])
        with c1:
            values = get_values(values)
        with c2:
            weights = get_weights(weights)

        sack_size = st.number_input("Enter sack size",min_value=1,max_value=100,value=15)
        st.caption("""<div style="text-align:center">
                    <p>Click submit to calculate the best case</p>
                    </div>""", unsafe_allow_html=True)
        co1,co2,co3 = st.columns([1.5,1,1.5])
        zo_submit = co2.form_submit_button("submit",use_container_width=True)


    df_01,hea = removing(weights,values,kd,sack_size)
    dfs_01 = zo(df_01,sack_size)

    with zo_col2.container(height=620):
        if hea ==1:
            st.error("Null (values/weights) or larger than the sack's size, please enter valid (values/weights).")
        else:
            max_value = dfs_01['Total Values'].max()
            count_max_value = dfs_01['Total Values'].eq(max_value).sum()
            visuals(dfs_01)
            first_n_values = dfs_01['Total Weights'].head(count_max_value)
            are_equal = first_n_values.nunique() == 1
            if are_equal:
                st.dataframe(dfs_01.head(count_max_value),use_container_width=True)
            else:
                dfs_01 = dfs_01[dfs_01["Total Weights"] == dfs_01.iloc[0]["Total Weights"]]
                st.dataframe(dfs_01.head(count_max_value),use_container_width=True)

def Unbound_knap(kd):
    values = []
    weights = []
    unb_col1, unb_col2 = st.columns([1,1],gap="large")
    with unb_col1.container(height=620,border=True).form("unbound_form",border=False):
        c1,c2=st.columns([1,1])
        with c1:
            values = get_values(values)
        with c2:
            weights = get_weights(weights)
        sack_size = st.number_input("Enter sack size",min_value=1,max_value=100,value=15)

        st.caption("""<div style="text-align:center">
                    <p>Click submit to calculate the best case</p></div>""", unsafe_allow_html=True)
        co1,co2,co3 = st.columns([1.5,1,1.5])
        unb_submit = co2.form_submit_button("submit",use_container_width=True)
    df_02, hea = removing(weights,values,kd,sack_size)
    if check_weights(weights, sack_size) and 0 not in values:
        dfs_unb = unb(df_02,sack_size)
    else:
        hea = 1
    with unb_col2.container(height=620,border=True):
        if hea ==1:
            st.error("Null (values/weights) or larger than the sack's size, please enter valid (values/weights).")
        else:
            dfs1 = dfs_unb.sort_values(by=["Total Values","Total Weights"], ascending=[False,True])
            max_value = dfs1['Total Values'].max()
            count_max_value = dfs1['Total Values'].eq(max_value).sum()
            visuals(dfs1)
            first_n_values = dfs1['Total Weights'].head(count_max_value)
            are_equal = first_n_values.nunique() == 1
            if are_equal:
                if count_max_value>10:
                    st.dataframe(dfs1.head(10),use_container_width=True)
                else:
                    st.dataframe(dfs1.head(count_max_value),use_container_width=True)
            else:
                dfs1 = dfs1[dfs1["Total Weights"] == dfs1.iloc[0]["Total Weights"]]
                if count_max_value>10:
                    st.dataframe(dfs1.head(10),use_container_width=True)
                else:
                    st.dataframe(dfs1.head(count_max_value),use_container_width=True)