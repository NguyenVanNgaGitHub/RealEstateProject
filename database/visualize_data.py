import pandas as pd
import numpy as np
from database import DataBase

class Visualize:

    @staticmethod
    def build_data_visualize():
        field_names = ['_id', 'time', 'district', 'wards', 'price', 'square']
        data = DataBase.get_all_data(field_names=field_names)

        data_dict = {}
        for field_name in field_names:
            data_dict[field_name] = []

        for ele in data:
            data_dict['_id'].append(str(ele['_id']))
            data_dict['district'].append(ele['district'])
            data_dict['wards'].append(ele['wards'])
            data_dict['price'].append(ele['price'])
            data_dict['square'].append(ele['square'])
            data_dict['time'].append(ele['time'])

        data = pd.DataFrame(data_dict)

        print(len(data))
        print(data)

        data.to_csv('mini-data.csv')

        # Build in here

        data['time'] = pd.to_datetime(data['time'])
        data.dtypes

        # So bai viet tren tung quan
        district_count = data.groupby('district').agg({"_id": "count"})
        district_count.to_csv('number-docs-per-district.csv')

        # So luong bai viet, gia, dien tich cua tung quan theo tung thang
        data['month'] = data['time'].dt.month
        data['year'] = data['time'].dt.year
        data_time = data.groupby(['year', 'month', 'district']).agg({"_id": "count", "price": "mean", "square": "mean"})
        data_time.to_csv('time-visualize.csv')

        # Gia, dien tich theo tung thang
        timeMean = data.groupby(['year', 'month']).agg({"price": "mean", "square": "mean"})
        timeMean.to_csv('timeMean.csv')

    @staticmethod
    def generate_statistic_district():
        # df_time_number_doc = pd.read_csv('time_number_doc.csv', index_col=['year', 'month', 'district'])
        # df_time_mean_price = pd.read_csv('time_mean_price.csv', index_col=['year', 'month', 'district'])
        # df_time_mean_square = pd.read_csv('time_mean_square.csv', index_col=['year', 'month', 'district'])
        df_time = pd.read_csv('time-visualize.csv', index_col=['year', 'month', 'district'])
        data_dict = {}
        for index in df_time.index:
            year = index[0]
            month = index[1]
            district = index[2]
            number_docs = df_time.loc[index]['_id']
            mean_price = df_time.loc[index]['price']
            mean_square = df_time.loc[index]['square']

            ym = str(year) + str(month)
            if ym not in data_dict:
                data_dict[ym] = {}
            data_dict[ym][district] = {}
            data_dict[ym][district]['num'] = number_docs
            data_dict[ym][district]['price'] = mean_price
            data_dict[ym][district]['square'] = mean_square
        data_dict

        # dict_time_number_doc = Visualize.build_dict(df_time_number_doc, '_id')
        # dict_time_mean_price = Visualize.build_dict(df_time_mean_price, 'price')
        # dict_time_mean_square = Visualize.build_dict(df_time_mean_square, 'square')

        db = DataBase.connect_to_database()
        # db.TimeNumberDoc.insert_one(dict_time_number_doc)
        # db.TimeMeanPrice.insert_one(dict_time_mean_price)
        # db.TimeMeanSquare.insert_one(dict_time_mean_square)
        db.TimeVisualize.insert_one(data_dict)

    @staticmethod
    def generate_statistic_time():
        df_time_mean = pd.read_csv('timeMean.csv', index_col=['year', 'month'])
        dict_time_mean = {}
        for index in df_time_mean.index:
            year = index[0]
            month = index[1]
            label = str(year) + str(month)
            if label not in dict_time_mean:
                dict_time_mean[label] = {}
            row = df_time_mean.loc[index]
            dict_time_mean[label]['price'] = row['price']
            dict_time_mean[label]['square'] = row['square']

        db = DataBase.connect_to_database()
        db.TimeMean.insert_one(dict_time_mean)


if __name__ == '__main__':
    Visualize.build_data_visualize()
    Visualize.generate_statistic_district()
    Visualize.generate_statistic_time()