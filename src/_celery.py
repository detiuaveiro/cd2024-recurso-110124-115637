from celery import Celery

app = Celery('sudoku_solver',
            broker='pyamqp://guest@localhost//',
            backend='redis://localhost:6379/0',
            include=['tasks'])

app.conf.update(
    task_serializer='json', 
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Lisbon',
    enable_utc=True,
)


app.conf.task_acks_late = True 
