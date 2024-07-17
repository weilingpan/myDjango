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

from enum import Enum

class JobStatusEnum(Enum):
    finish = FinishedJobRegistry #已完成的任務
    failed = FailedJobRegistry #失敗的任務
    started = StartedJobRegistry #正在進行的任務
    deferred = DeferredJobRegistry #被推遲的任務
    scheduled = ScheduledJobRegistry #計畫中的任務


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

def get_jobs(status: str):
    queue = django_rq.get_queue('default')
    registry_map = {
        JobStatusEnum.finish.name: FinishedJobRegistry,
        JobStatusEnum.failed.name: FailedJobRegistry,
        JobStatusEnum.started.name: StartedJobRegistry,
        JobStatusEnum.deferred.name: DeferredJobRegistry,
        JobStatusEnum.scheduled.name: ScheduledJobRegistry
    }
    
    job_registry_class = registry_map.get(status)
    if job_registry_class:
        job_registry = job_registry_class(queue=queue)
        job_ids = job_registry.get_job_ids()
        jobs = [Job.fetch(job_id, connection=queue.connection) for job_id in job_ids]
        return job_ids, jobs
    else:
        raise ValueError(f"Invalid job status: {status}")
