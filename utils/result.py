import os
import sys
import datetime
from typing import Any
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)
from utils.elasticsearch.elastic_engine import ESEngine

class Reporting:
    def __init__(self, job: str, es: Any = None):
        self.job = job
        self.start_time = datetime.datetime.now(datetime.timezone.utc)
        self.end_time = None
        self.es = es if es else ESEngine()
        self.es_index = 'symphony_job_schedule'

    def __str__(self):
        return f'Job Name: {self.job},\nStart time: {self.start_time},\nEnd time: {self.end_time}'

    def set_end_time(self):
        self.end_time = datetime.datetime.now(datetime.timezone.utc)

    def report_result(self, result: str, error: str = None):
        self.set_end_time()
        error_mapping = {
            'read': '데이터를 불러오는 데 실패하였습니다.',
            'write': '데이터를 저장하는 데 실패하였습니다.',
            'exist': '데이터가 존재하지 않습니다.',
            'connect': 'DB 연결에 실패하였습니다.'
        }

        data = {
            'job': self.job,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'result': result,
            'error': error_mapping.get(error, error) if error and result == 'fail' else '없습니다.'
        }

        self.es.write_data(data=data, index=self.es_index)

    @staticmethod
    def retrieve_current_time():
        return datetime.datetime.now(datetime.timezone.utc)