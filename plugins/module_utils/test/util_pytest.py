from datetime import datetime

FILE_TEST_LOG = '/tmp/ansible-opnsense-test.log'


def log_test(msg: str):
    with open(FILE_TEST_LOG, 'a+', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {msg}" + '\n')
