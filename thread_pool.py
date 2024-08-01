import concurrent.futures
from datetime import datetime
import time
import os

cpu_count = os.cpu_count()
max_workers = cpu_count * 2
print(f"Using max_workers: {max_workers}")

# 0*10 + 1*10 + 2*10 = 0+10+20 = 30
#  縮短成 20 s

# 0*10 + 1*10 + 2*10 + 3*10 = 0+10+20+30 = 60
#  縮短成 30 s

def download_file(i):
    print(f"[{datetime.now()}] download {i} ...")
    time.sleep(i*10)
    print(f"[{datetime.now()}] download {i} done")
    return f"job {i}"

def process_file(job):
    print(f"[{datetime.now()}] process {job} ...")

# 使用 ThreadPoolExecutor 进行多线程下载
def download_and_process_files():
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_file, i): i for i in range(4)}
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                process_file(result)
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_and_process_files()