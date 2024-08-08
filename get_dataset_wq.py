import requests
import json
import os
import config as cf
import schedule
import time
from multiprocessing import Pool, cpu_count
import pandas as pd
from utils.create_table import create_table_data
from sqlalchemy import create_engine

class DatasetWQ:
    def __init__(self, dataset):
        self.dataset = dataset
        self.region = cf.region
        self.universe = cf.universe
        self.delay = cf.delay
        self.path_token = cf.path_token
        self.path_dataset = cf.path_dataset.format(self.region,self.dataset)
        self.token = self.read_token()
        self.dataset_information = cf.api_dataset_information.format(self.dataset)
        self.url_dataset = cf.api_dataset
        self.option = None
        self.alpha_count = int(cf.alpha_count)
        self.coverage = float(cf.coverage)

    def read_token(self):
        # read token from txt file
        if os.path.exists(self.path_token):
            with open(self.path_token) as f:
                lines = f.readlines()
            token = lines[0]
            return str(token)
        else:
            print("Đường dẫn token không tồn tại, kiểm tra lại đường dẫn!")
            return 0

    def count_field_dataset(self):
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + self.token
        }
        dataset = requests.request("GET", self.dataset_information, headers=headers, data=payload)
        if dataset.status_code == 200:
            json_data = json.loads(dataset.text)
            print("Tên bộ dữ liệu: {} ({})".format(json_data['name'], self.dataset))
            for data_ in json_data['data']:
                if data_['region'] == self.region and data_['universe'] == self.universe:
                    print("Điểm của bộ dữ liệu: {}".format(data_['valueScore']))
                    print("Số lượng data trong bộ dữ liệu: {}".format(data_['fieldCount']))
                    return int(data_['fieldCount'])
        else:
            print("Kiểm tra tên bộ dữ liệu hoặc token!")
            return 0

    def get_dataset_wq(self):
        data = []
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + self.token
        }
        number_data = self.count_field_dataset()
        offset = [i for i in range(0, number_data, 50)]
        for i in offset:
            url_dataset = self.url_dataset.format(str(self.dataset),
                                                  str(self.delay),
                                                  str(i),
                                                  str(self.region),
                                                  str(self.universe))
            dataset = requests.request("GET", url_dataset, headers=headers, data=payload)
            if dataset.status_code == 200:
                data.append(json.loads(dataset.text))
            else:
                print("Lỗi lấy dữ liệu!")
                return 0
        return data

    def insert_into_database(self, data_json):
        data_dict = {
            'dataField': [],
            'dataset': [],
            'type': [],
            'coverage': [],
            'userCount': [],
            'alphaCount': [],
            'region': [],
            'delay': [],
            'universe': [],
        }
        for json_data in data_json:
            for attribute in json_data["results"]:
                data_dict['dataField'].append(attribute['id'])
                data_dict['dataset'].append(self.dataset)
                data_dict['type'].append(attribute['type'])
                data_dict['coverage'].append(attribute['coverage'])
                data_dict['userCount'].append(attribute['userCount'])
                data_dict['alphaCount'].append(attribute['alphaCount'])
                data_dict['region'].append(attribute['region'])
                data_dict['delay'].append(attribute['delay'])
                data_dict['universe'].append(attribute['universe'])
        df = pd.DataFrame(data_dict)
        df.columns = df.columns.str.lower()
        engine = create_engine(cf.CONNECTION_STRING)
        df.to_sql('data', engine, if_exists='append', index=False)

    def process_dataset(self):
        dataset = self.get_dataset_wq()
        create_table_data()
        self.insert_into_database(dataset)
        attribute = []
        for json_data in dataset:
            if self.option is None:
                for data in json_data["results"]:
                    if data["alphaCount"] >= int(self.alpha_count):
                        if data["type"] == "VECTOR":
                            attribute.append("vec_avg(" + data["id"] + ")")
                        if data["type"] == "MATRIX":
                            attribute.append(data["id"])
            else:
                for data in json_data["results"]:
                    if data['coverage'] >= float(self.coverage) and data["alphaCount"] >= int(self.alpha_count):
                        if data["type"] == "VECTOR":
                            attribute.append("vec_avg(" + data["id"] + ")")
                        if data["type"] == "MATRIX":
                            attribute.append(data["id"])
        print("Số lượng trường dữ liệu thoả mãn điều kiện:{}".format(len(attribute)))
        return attribute

    def save_dataset(self):
        attribute = self.process_dataset()
        with open("{}.txt".format(self.path_dataset), "w", encoding='utf-8') as txt_file:
            for line in attribute:
                txt_file.write("".join(line) + "\n")
        print("Dữ liệu được lưu trữ tại: {}".format(self.path_dataset + ".txt"))

def run_multiprocess(data):
    wq_dataset = DatasetWQ(data)
    wq_dataset.save_dataset()

def job():
    with Pool(processes=10) as pool:
        pool.map(run_multiprocess, cf.dataset)
    pool.close()

if __name__ == '__main__':
    job()