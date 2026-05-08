"""
项目：文件通信式双AI协作Agent（稳定版）
架构规划：DeepSeek V4
任务执行：Claude
"""
import os
import re
from datetime import datetime

TASK_FILE = "next_action.md"
RULE_FILE = "协议.md"
LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

def write_log(text):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(LOG_DIR, "run.log"), "a", encoding="utf-8") as f:
        f.write(f"[{now}] {text}\n")

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def update_task(task_id, status, result):
    content = read_file(TASK_FILE)
    # 定位任务块
    pattern = re.compile(r"## " + task_id + r".*?(?=## |\Z)", re.DOTALL)
    task_block = pattern.search(content)
    if not task_block:
        write_log(f"找不到任务块：{task_id}")
        return
    
    # 更新状态和结果
    new_block = task_block.group(0)
    new_block = re.sub(r"执行状态：.*", f"执行状态：{status}", new_block)
    new_block = re.sub(r"执行结果：.*", f"执行结果：{result}", new_block)
    
    # 替换回原内容
    new_content = content.replace(task_block.group(0), new_block)
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    write_log(f"{task_id} 状态更新为：{status}，结果已回填")

def main():
    print("===== Claude 执行Agent 启动 =====")
    write_log("Agent启动成功")

    # T001
    print("正在执行 T001 项目目录自检")
    files = os.listdir("./")
    res1 = f"项目目录扫描完成，现有文件：{files}"
    update_task("任务T001", "执行中", res1)
    update_task("任务T001", "已完成", res1)
    print("T001 执行完毕\n")

    # T002
    print("正在执行 T002 协议文档数据分析")
    rule_text = read_file(RULE_FILE)
    res2 = f"协议.md总字符数：{len(rule_text)}"
    update_task("任务T002", "执行中", res2)
    update_task("任务T002", "已完成", res2)
    print("T002 执行完毕\n")

    # T003
    print("正在执行 T003 文本内容词数统计")
    task_text = read_file(TASK_FILE)
    res3 = f"任务清单文档总长度：{len(task_text)}"
    update_task("任务T003", "执行中", res3)
    update_task("任务T003", "已完成", res3)
    print("T003 执行完毕\n")

    print("===== 所有任务执行完成 =====")
    write_log("所有任务执行完毕")

if __name__ == "__main__":
    main()