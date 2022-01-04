import datetime
import pandas as pd


class Data:

    def __init__(self):
        self.plant_data = pd.read_excel(
            'C:/Users/Bugra/Desktop/dash_data_kasım/kgup_cost-2021-11.xlsx',
            index_col=0, sheet_name='All')
        self.grup_data = pd.read_excel(
            'C:/Users/Bugra/Desktop/dash_data_kasım/imbalance_cost_w-2021-11.xlsx',
            index_col=0, sheet_name='All')
        self.ptf_smf = pd.read_excel(
            'C:/Users/Bugra/Desktop/dash_data_kasım/ptf_smf.xlsx',
            index_col=0)


    @staticmethod
    def append_ptf_smf(ptf_smf):
        ptf_smf = ptf_smf[['mcp', 'smp']].max(axis=1).resample('M').mean().to_frame().rename(
            columns={0: 'Max_PTF_SMF'}).reset_index()
        ptf_smf['date'] = pd.to_datetime(ptf_smf['date']).dt.strftime('%Y-%m')
        return ptf_smf.set_index('date')

    def prepare_group_data(self):
        self.grup_data['Date'] = pd.to_datetime(self.grup_data[['Year', 'Month']].assign(Day=1)).dt.strftime('%Y-%m')

        self.grup_data.loc[self.grup_data['Grup'] == 'company', 'Name'] = \
            self.grup_data.loc[self.grup_data['Grup'] == 'company', 'Name'].str.cat(
                '-' + self.grup_data.loc[self.grup_data['Grup'] == 'company', 'Grup'])

        self.grup_data = self.grup_data[['Date', 'Üretim', 'KÜPST', 'Grup']].groupby(
            ['Date', 'Grup']).sum().reset_index()

        self.grup_data['WA Kgüp Maliyeti'] = (self.grup_data['KÜPST'] / self.grup_data['Üretim'])
        self.grup_data = self.grup_data.pivot(index='Date', columns='Grup', values='WA Kgüp Maliyeti')
        ptf_smf_data = self.append_ptf_smf(self.ptf_smf)
        self.grup_data = pd.concat([self.grup_data, ptf_smf_data], axis=1)
        return self.grup_data.round(2).reset_index().rename(columns={'index': 'date'})

    def prepare_plant_data(self):
        self.plant_data.index = pd.to_datetime(self.plant_data.index).strftime('%Y-%m')
        ptf_smf_data = self.append_ptf_smf(self.ptf_smf)
        self.plant_data = pd.concat([self.plant_data, ptf_smf_data], axis=1)
        return self.plant_data.round(2).reset_index()
