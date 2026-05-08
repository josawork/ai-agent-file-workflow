"""
项目：文件通信式双AI协作Agent
架构规划：DeepSeek V4
任务执行：Claude
功能：任务读取、自动化执行、状态更新、结果回写、运行日志记录
"""
import os
import configparser
from datetime import datetime

# 读取配置文件
cfg = configparser.ConfigParser()
cfg.read("config.ini", encoding="utf-8")

TASK_FILE = cfg["PATH"]["task_file"]
RULE_FILE = cfg["PATH"]["rule_file"]
LOG_DIR = cfg["PATH"]["log_dir"]

# 创建日志文件夹
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

def write_log(text):
    """写入运行日志"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = os.path.join(LOG_DIR, "run.log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {text}\n")

def read_md(file_path):
    """读取md文档全部内容"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def update_task_result(task_file, task_id, status, result):
    """更新任务状态，回写执行结果"""
    content = read_md(task_file)
    content = content.replace(f"{task_id}\n执行状态：待执行", f"{task_id}\n执行状态：{status}")
    content = content.replace("执行结果：暂无", f"执行结果：{result}", 1)
    with open(task_file, "w", encoding="utf-8") as f:
        f.write(content)
    write_log(f"{task_id} 状态变更为：{status}，执行结果已回填")

def main():
    banner = "===== Claude 执行Agent 启动，接收DeepSeek V4规划任务 ====="
    print(banner)
    write_log("Agent启动成功，开始接收规划任务")

    # 执行任务T001
    print("正在执行任务 T001 项目目录自检")
    file_list = os.listdir("./")
    res1 = f"项目目录扫描完成，现有文件列表：{file_list}"
    update_task_result(TASK_FILE, "任务T001", "执行中", res1)
    update_task_result(TASK_FILE, "任务T001", "已完成", res1)
    print("T001 执行完毕\n")

    # 执行任务T002
    print("正在执行任务 T002 协议文档数据分析")
    rule_text = read_md(RULE_FILE)
    res2 = f"协议.md总字符数：{len(rule_text)}"
    update_task_result(TASK_FILE, "任务T002", "执行中", res2)
    update_task_result(TASK_FILE, "任务T002", "已完成", res2)
    print("T002 执行完毕\n")

    # 执行任务T003
    print("正在执行任务 T003 文本内容词数统计")
    task_text = read_md(TASK_FILE)
    res3 = f"任务清单文档文本总长度：{len(task_text)}"
    update_task_result(TASK_FILE, "任务T003", "执行中", res3)
    update_task_result(TASK_FILE, "任务T003", "已完成", res3)
    print("T003 执行完毕\n")

    end_text = "===== 所有DeepSeek V4规划任务，Claude全部执行完成 ====="
    print(end_text)
    write_log("所有任务执行完毕，Agent待机结束")

if __name__ == "__main__":
    main()