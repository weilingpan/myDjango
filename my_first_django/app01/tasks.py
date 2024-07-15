import time
from django_rq import job
from datetime import datetime

# 創建一個異步任務
@job
def example_task(data):
    print(f"~~~~~~ {datetime.now()}")
    time.sleep(15)
    print(f"~~~~~~Task completed with data: {data}")
    print(f"~~~~~~ {datetime.now()}")
    # 可以觀看 redis 裡面的資料變化
