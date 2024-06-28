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
    broker_connection_retry_on_startup=True, # retry connection on startup
    worker_prefetch_multiplier=1, # 1 task per worker
    worker_concurrency=1, # 1 worker
    # worker_max_tasks_per_child=1, # worker will be restarted after 1 task
    task_reject_on_worker_lost=True, # reject task if worker is lost, so it can be retried by another worker

)


app.conf.task_acks_late = True 
