import time
import csv
from threading import Thread
import code128

class CasualtyLogger:
    def __init__(self, initial=0, increase=200, filename="casualty_log.csv"):
        self.count = initial
        self.increase = increase
        self.filename = filename
        self.running = False
        self._setup_file()

    def _setup_file(self):
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "DateTime", "Casualties"])

    def _log_entry(self):
        timestamp = time.time()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, current_time, self.count])
        print(f"记录: {current_time} - {self.count}")

    def _update(self):
        while self.running:
            self._log_entry()
            code128.image(self.count).save("casualty_log.png")
            time.sleep(10)
            self.count += self.increase

    def start(self):
        self.running = True
        Thread(target=self._update).start()

    def stop(self):
        self.running = False
        self._log_entry()  # 确保最后一次更新被记录


# 使用示例
logger = CasualtyLogger(initial=1, increase=300, filename="../war_casualties.csv")
logger.start()

# 让程序运行一段时间后停止
time.sleep(1800)  # 30分钟后
logger.stop()






