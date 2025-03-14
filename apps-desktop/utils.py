import random
import string
import pandas as pd


def generate_fake_data():
    list_data = []
    for i in range(1000):
        list_data.append({
            'name': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
            'age': random.randint(18, 99),
            'date': '2020-01-01',
            'address': 'Calle 123',
            'city': 'Bogota',
            'country': 'Colombia',
            'email': 'example@gmail.com'
        })

    return pd.DataFrame(list_data)

def read_data_sample_csv(path):
    return pd.read_csv(path)


dir_data = '/home/engineer/internet/downloads/business-employment-data-Jun-2024-quarter/'
df = read_data_sample_csv(dir_data + 'Jun-2024-quarter1.csv')

df.to_csv(dir_data+'Jun-2024-quarter1.csv.gz', index=False, compression='gzip')

df.to_parquet(dir_data+'Jun-2024-quarter1.parquet', index=False)