import django_rq
from rq.job import Job

# 用於查詢不同狀態的jobs
from rq.registry import (
    FinishedJobRegistry, #已完成的任務
    FailedJobRegistry, #失敗的任務
    StartedJobRegistry, #正在進行的任務
    DeferredJobRegistry, #被推遲的任務
    ScheduledJobRegistry #計畫中的任務
    )

"""
django_rq 的一些用法
"""
# scheduler = django_rq.get_scheduler()

def get_finished_jobs():
    queue = django_rq.get_queue('default')
    finished_job_registry = FinishedJobRegistry(queue=queue)
    job_ids = finished_job_registry.get_job_ids()
    jobs = [Job.fetch(job_id, connection=queue.connection) for job_id in job_ids]
    return job_ids, jobs
