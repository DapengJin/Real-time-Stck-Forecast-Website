# author: Yixuan Duan
import pandas as pd


class DataManager:
    def __init__(self, file_path):
        self._data = pd.read_csv(file_path)
        self._back_up = self._data.copy()
      
    def load_dataframe(self, df):
        self._data = df

    def group_sales_by(self, column_name):
        try:
            self._data = self._data.groupby(column_name, as_index=False).sum()
        except KeyError:
            print(f'Column \'{column_name}\' does not exsist')
            return
        
        for c in self._data.columns:
            if '_Sales' in c or c in column_name:
                pass
            else:
                del self._data[c]

    def filter_by_list(self, column_name, filter_list):
        try:
            self._data = self._data.loc[self._data[column_name].isin(filter_list), :]
        except KeyError:
            print(f'Column \'{column_name}\' does not exsist')

    def filter_by_range(self, column_name, min_val, max_val, include_max=True):
        try:
            if include_max:
                self._data = self._data.loc[(self._data[column_name] >= min_val) & (self._data[column_name] <= max_val), :]
            else:
                self._data = self._data.loc[(self._data[column_name] >= min_val) & (self._data[column_name] < max_val), :]
        except KeyError:
            print(f'Column \'{column_name}\' does not exsist')

    def sort(self, column_name, ascending=True):
        try:
            self._data = self._data.sort_values(by=column_name, ascending=ascending)
        except KeyError:
            print(f'Column \'{column_name}\' does not exsist')
    
    def reset_data(self):
        self._data = self._back_up

    def get_data(self):
        return self._data

    @property
    def data(self):
        return self._data

    @property
    def column_names(self):
        return list(self._data.columns)