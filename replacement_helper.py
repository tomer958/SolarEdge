import pandas as pd
from datasource_helper import DataSource

class ReplacemntDecicder:
    
    """
    This class is the engine that is responsible to return to the user the compatible part and quantity,\
        given `part` and `geo`.

    Params:
    ---
    :param: `part` -> The part name that should be replaced.
    """

    df_source = DataSource('Service BI Analyst - Home Assignment.xlsx')
    df_compatability = df_source.get_compatability()
    df_inventory = df_source.get_inventory()

    def __init__(self,
                part: str,
                geo: str = None
                ) -> None:
        # Validations for `part` attribute.
        if len(part) == 0:
            raise ValueError("Expeceting power, got None.")
        if not isinstance(part, str):
            raise ValueError(f"Exepected string, got value: {part} of type: {type(part)}")
        if len(part.split('-'))==1:
            raise ValueError("Expected full part name with hypens")
        self.part = part
        
        if geo:    
            if not isinstance(geo, str):
                raise ValueError(f"Exepected string, got value: {geo} of type: {type(geo)}")
            
            if geo not in self.locations:
                raise ValueError(f"geo is not exists. Provide one geo from: {self.locations}")
        self.geo = geo

    @staticmethod
    def locations_prompt() -> list:
        return ['ROW', 'Europe', 'US']
    
    @property
    def locations(self) -> list:
        return self.locations_prompt()

    def __get_compatible_parts(self) -> pd.DataFrame:
        power = self.part.split('-')[0]
        df_compatible_parts = self.df_compatability[self.df_compatability['power_idx']==power]
        return df_compatible_parts

    def get_qty(self) -> pd.DataFrame:
        df_filtered = self.__get_compatible_parts()
        df_joined = self.df_inventory.merge(
                        df_filtered,
                        how='inner',
                        left_on='Power',
                        right_on='power'
                        )
        df_joined = df_joined.sort_values(by=['qty'], ascending=False) if not self.geo else \
                    df_joined.sort_values(by=['qty'], ascending=False)[df_joined['geo']==self.geo]
        return df_joined[['power', 'qty', 'geo']]
