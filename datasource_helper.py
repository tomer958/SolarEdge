import pandas as pd

class DataSource:
    """
    This class represents a connection to the database and holds extarction and transformation methods.
    """
    def __init__(self,
                path: str
                ) -> None:
        
        if len(path) == 0:
            raise AssertionError("Expeceting path for file, got None.")
        if not isinstance(path, str):
            raise ValueError(f"Exepected string, got value: {path} of type: {type(path)}")
        self.path = path

    def get_compatability(self) -> pd.DataFrame:
        df = pd.read_excel(self.path, sheet_name=0)
        columns = [val for val in df.columns if val != 'Unnamed: 0'] # Collect columns.
        flaten_df = pd.melt(df, id_vars=['Unnamed: 0'], value_vars=columns, var_name='power', value_name='match') #Flattening df from pivot struct.
        flaten_df = flaten_df.rename(columns={'Unnamed: 0': 'power_idx'}) 
        flaten_df = flaten_df[flaten_df['match']=='ü'] # Saving only compatible powers.
        return flaten_df[['power_idx','power']]
    
    def get_inventory(self) -> pd.DataFrame:
        df = pd.read_excel(self.path, sheet_name=1)
        columns = [val for val in df.columns] # Collect columns.
        df.ROW = df.ROW.astype(int) #Assuming ROW = rest of world. Casting from float to int. 
        flaten_df = pd.melt(df, id_vars=['Power'], value_vars=columns, var_name='geo',value_name='qty') #Flattening df from pivot struct.
        return flaten_df

    def get_component(self) -> pd.DataFrame:
        df = pd.read_excel(self.path, sheet_name=2)
        df = df.rename(columns={'Component:': 'component'})
        return df