import datetime
import os

import requests
from django.core.management.base import BaseCommand
from tqdm import tqdm

from conf.settings import BASE_DIR
from logs.models import LogItem


class Command(BaseCommand):
    """Command for parse Apache Logs"""
    DEFAULT_LOG_URL = 'http://www.almhuette-raith.at/apache-log/access.log'

    DATE_PATTERN = '%d/%b/%Y:%H:%M:%S %z'
    FILE_PATH = os.path.join(BASE_DIR, 'access.log')
    CHUNK_SIZE = 1024
    MASS_SAVE_COUNT = 1000
    MAX_CHARS = 300
    VALID_METHODS = ['POST', 'GET', 'HEAD', 'PUT', 'DELETE' 'OPTION']

    help = "parse apache logs from url"

    def add_arguments(self, parser):
        parser.add_argument('--url', help='url to log file', default=self.DEFAULT_LOG_URL)
        super().add_arguments(parser)

    def handle(self, *args, **options):
        url = options.get('url')
        if not self.is_text_file(url):
            self.stdout = 'is not log file'
            return

        self.download_file(url)

        log_count = self.get_log_count()
        self.save_logs(log_count)
        self.stdout = f'{log_count} log records'

        self.remove_file()

    def is_text_file(self, url):
        resp = requests.head(url)
        return 'text' in resp.headers.get('content-type')

    def download_file(self, url):
        """Download log file with progressbar"""
        resp = requests.get(url, stream=True)
        file_size = int(resp.headers['Content-Length'])
        with open(self.FILE_PATH, 'wb') as f:
            with tqdm(total=file_size / self.CHUNK_SIZE, desc='log file downloading', ) as pbar:
                for chunk in resp.iter_content(chunk_size=self.CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        pbar.update(1)

    def remove_file(self):
        os.remove(self.FILE_PATH)

    def get_log_count(self):
        """Get count of records in log file"""
        with open(self.FILE_PATH) as log_file:
            return sum(1 for __ in log_file)

    def save_logs(self, log_count):
        """Save log records in LogItem model with mass save"""
        with open(self.FILE_PATH) as log_file:
            with tqdm(total=log_count, desc='save to database', ) as pbar:
                record_list = []
                record_count = 1
                for line in log_file:

                    record = self.parse_line(line)
                    if record is None:
                        continue
                    record_list.append(LogItem(
                        ip=record['ip'],
                        datetime=self.parse_date(record['date']),
                        method=record['method'],
                        uri=record['uri'],
                        status_code=record['status'],
                        body_size=record['body_size'],
                        user_agent=record['agent']
                    ))

                    if record_count == self.MASS_SAVE_COUNT:
                        LogItem.objects.bulk_create(record_list)
                        record_list = []
                        record_count = 0
                    pbar.update(1)
                    record_count += 1

    def parse_date(self, date):
        return datetime.datetime.strptime(date, self.DATE_PATTERN)

    def parse_line(self, line):
        """
        Log record parsing with split to list
        :param line: log record
        :return: log data in dict
        """
        record = line.split()
        if len(record) > 11:
            return {
                'ip': record[0],
                'date': f"{record[3][1:]} {record[4][:-1]}",
                'method': self._get_method(record[5]),
                'uri': record[6][:self.MAX_CHARS],
                'status': record[8],
                'body_size': record[9] if record[9].isdigit() else 0,
                'agent': ' '.join(record[11:-1])[:self.MAX_CHARS],
            }

    def _get_method(self, method):
        if len(method) <= 8:
            method = method[1:].upper()
            if method in self.VALID_METHODS:
                return method
        for op in self.VALID_METHODS:
            if method.endswith(op):
                return op
        return 'UNKNOWN'
