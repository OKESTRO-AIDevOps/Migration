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
        """Creating Reporting tool.

        Args:
            job (str): name of job. (ex.anomaly_detection, prediction ...)
            start_time (str): start time 
            end_time (str, optional): end time. if None, same to start time. Defaults to None.
        """
        # job info
        self.job = job
        if start_time:
            self.start_time = start_time
        else:
            self.start_time = self.retrieve_current_time()
        self.end_time = end_time
        # init elastic engine
        if es:
            self.es = es
        else:
            self.es = ESEngine()
        self.es_index = 'symphony_job_schedule'

    def __str__(self):
        return f'Job Name : {self.job},\nStart time : {self.start_time},\nEnd:time : {self.end_time}'

    def set_start_time(self):
        """Set start time to current UTC time."""
        self.start_time = datetime.datetime.now(datetime.timezone.utc)
    
    def set_end_time(self):
        """Set end time to current UTC time."""
        self.end_time = datetime.datetime.now(datetime.timezone.utc)