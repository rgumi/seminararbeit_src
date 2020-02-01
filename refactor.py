import pandas as pd



dates = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Mär': '03',
    'Apr': '04',
    'May': '05',
    'Mai': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Okt': '10',
    'Nov': '11',
    'Dec': '12',
    'Dez': '12'
}
def euribor():
    raw_data = pd.read_csv("raw/euribor3m_raw.csv", sep=';')
    raw_data.loc[:, 'date'] = raw_data.loc[:, 'period'].apply(lambda x: f'{x[:4]}-{dates[x[4:]]}-01')
    raw_data.drop('period', axis=1, inplace=True)
    raw_data['date'] = pd.to_datetime(raw_data['date'])

    data = raw_data.loc[(raw_data['date'].dt.year > 2007)]
    data = data.sort_values(by=['date'])
    data.reset_index(drop=True, inplace=True)
    data.to_csv('refined/euribor3m_ref.csv', index_label='index')

def cpi():
    raw_data = pd.read_csv("raw/cpi_monthly_raw.csv", sep=',', parse_dates=['TIME'])

    # Select only values from the eurozone (https://de.wikipedia.org/wiki/Eurozone)
    data = raw_data.loc[(raw_data['LOCATION'] == 'EA19')]
    data = data.sort_values(by=['TIME'])
    data.reset_index(drop=True, inplace=True)
    data[['Value', 'TIME']].to_csv('refined/cpi_monthly_ref.csv', index_label='index')

def cci():
    raw_data = pd.read_csv("raw/cci_monthly_raw.csv", sep=',', parse_dates=['TIME'])

    # Select only values from the eurozone (https://de.wikipedia.org/wiki/Eurozone)
    data = raw_data.loc[(raw_data['LOCATION'] == 'EA19')]
    data = data.sort_values(by=['TIME'])
    data.reset_index(drop=True, inplace=True)
    data[['Value', 'TIME']].to_csv('refined/cci_monthly_ref.csv', index_label='index')

def eurostoxx():
    raw_data = pd.read_csv("raw/eurostoxx_raw.csv", sep=',')
    raw_data.drop(['Zuletzt', 'Eröffn.', 'Hoch', 'Tief', 'Vol.'], inplace=True, axis=1)
    raw_data.loc[:, 'date'] = raw_data.loc[:, 'Datum'].apply(lambda x: f'{x[4:]}-{dates[x[:3]]}-01')
    def get_value(val):
        return float(val.replace('%', '').replace(',', '.'))/100

    raw_data.loc[:, 'value'] = raw_data.loc[:, '+/- %'].apply(get_value)
    raw_data.drop(['Datum', '+/- %'], axis=1, inplace=True)

    data = raw_data.sort_values(by=['date'])
    data.reset_index(drop=True, inplace=True)
    data.to_csv('refined/eurostoxx_ref.csv', index_label='index')

def fsi():
    raw_data = pd.read_csv("raw/fsi_raw.csv", sep=',', parse_dates=['Date'])

    # Select only values from the eurozone (https://de.wikipedia.org/wiki/Eurozone)
    data = raw_data.loc[(raw_data['Date'].dt.year > 2007)]

    data = data.sort_values(by=['Date'])
    data.reset_index(drop=True, inplace=True)
    data.drop(['United States', 'Emerging markets', 'Other advanced economies'], inplace=True, axis=1)
    print(data.head())
    data.to_csv('refined/fsi_ref.csv', index_label='index')

fsi()