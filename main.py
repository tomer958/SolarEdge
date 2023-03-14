import pandas as pd
import streamlit as st
import time
from datasource_helper import DataSource
from replacement_helper import ReplacemntDecicder


def main(part_name: str, geo: str = None) -> pd.DataFrame:
    if geo:
        part = ReplacemntDecicder(part=part_name,geo=geo)
        result = part.get_qty()
    else:
        part = ReplacemntDecicder(part=part_name)
        result = part.get_qty()

    st.dataframe(result.head(3))


if __name__ == '__main__':

    st.title('SolarEdge- Powers replacement')

    label = """
        Choose part name:\n
        """
        
    df_source = DataSource('/Users/Tomer/Downloads/Service BI Analyst - Home Assignment.xlsx')
    df_components = df_source.get_component().to_dict()
    parts = [v for k,v in df_components['component'].items()]
    part_name_opt = st.selectbox(label=label, options=parts)
    with st.spinner('Proccessing...'):
        time.sleep(1)
    main(part_name=part_name_opt)
    
    
