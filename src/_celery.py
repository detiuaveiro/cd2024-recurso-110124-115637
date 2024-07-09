from celery import Celery


broker_urls = [
    'amqp://guest:guest@localhost:5672//',
    'amqp://guest:guest@localhost:5673//',
    'amqp://guest:guest@localhost:5674//',
    'amqp://guest@localhost//',  # default
]

app = Celery('sudoku_solver',
            broker=broker_urls,
            backend='redis://localhost:6379/0',
            include=['tasks'])

app.conf.update(
    task_serializer='json', 
    result_serializer='json',
    accept_content=['json'],
    timezone='Europe/Lisbon',
    enable_utc=True,
    # worker_concurrency=4, # 1 worker
    # worker_max_tasks_per_child=1, # worker will be restarted after 1 task

    # broker settings
    broker_connection_retry=True,
    broker_connection_max_retries=10, # or None 
    broker_connection_retry_interval_start=2,  
    broker_connection_retry_interval_step=2,  
    broker_connection_retry_interval_max=30,  
    broker_connection_retry_on_startup=True, # retry connection on startup

    # workers config
    worker_prefetch_multiplier=1, # 1 task per worker
    worker_cancel_long_running_tasks_on_connection_loss = True,
    worker_autoscale='5,1', # min 4 workers, max 1 worker
    task_reject_on_worker_lost=True, # reject task if worker is lost, so it can be retried by another worker


)


app.conf.task_acks_late = True 
