from celery import Celery

app = Celery('sudoku solver', broker='pyamqp://guest@localhost//', backend='rpc://')

app.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Lisbon',
    enable_utc=True,
)