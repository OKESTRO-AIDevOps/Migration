import os
import sys
import datetime
from typing import Any
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)
from utils.elasticsearch.elastic_engine import ESEngine

class Reporting(object):
    def __init__(self,
                job: str,
                es: Any=None,
                start_time: str=None,
                end_time : str=None):
        self.job = job
        if start_time:
            self.start_time = start_time
        else:
            self.start_time = self.retrieve_current_time()
        self.end_time = end_time
        if es:
            self.es = es
        else:
            self.es = ESEngine()
        self.es_index = 'symphony_job_schedule'

    def __str__(self):
        return f'Job Name : {self.job},\nStart time : {self.start_time},\nEnd:time : {self.end_time}'

    def set_start_time(self):
        self.start_time = datetime.datetime.now(datetime.timezone.utc)
    
    def set_end_time(self):
        self.end_time = datetime.datetime.now(datetime.timezone.utc)

    def retrieve_current_time(self):
        return datetime.datetime.now(datetime.timezone.utc)

    def report_result(self, 
                    result : str,
                    error: str=None):
        self.end_time = self.retrieve_current_time()  
        data = {
            "job": self.job,
            "start_time": self.start_time ,
            "end_time": self.end_time ,
            "result": result
            }
        if (not error) and (result =='success'):
            data['error'] = '없습니다.'
        elif error and result == 'fail':
            if error == 'read':
                data['error'] = '데이터를 불러오는 데 실패하였습니다.'
            elif error =='write': 
                data['error'] = '데이터를 저장하는 데 실패하였습니다.' 
            elif error == 'exist':
                data['error'] = '데이터가 존재하지 않습니다.'
            elif error == 'connect':
                data['error'] = 'DB 연결에 실패하였습니다.'
            else:
                data['error'] = error
        self.es.write_data(data=data, index=self.es_index)
