import pandas as pd
pv = pd.pivot_table(
        df,
        index=['steward'],
        columns=['health'],
        values=['count_tree_id'],
        aggfunc=sum,
        fill_value=0)

pv2 = pd.pivot_table(
        df2,
        index=['Name'],
        columns=["Status"],
        values=['Quantity'],
        aggfunc=sum,
        fill_value=0)