import streamlit as st
import pandas as pd

"# Hello"

df = pd.DataFrame({"a": [1,2,3], "b":[3,4,2], "c":[2,1,3]}).set_index('a')
st.line_chart(df)