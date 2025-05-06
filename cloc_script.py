import subprocess
import json
import matplotlib.pyplot as plt
import os

# 设置你的 Unity 项目路径
UNITY_PROJECT_PATH = "/Users/vanish/Desktop/DungeonPension/branches/dev_vanish/Assets/Scripts"  # 修改这里

# 执行 cloc 命令并将结果保存为 JSON 文件
def run_cloc(project_path, output_file="cloc_output.json"):
    try:
        subprocess.run([
            "cloc",
            project_path,
            "--json",
            "--out", output_file
        ], check=True)
        print(f"cloc 分析完成，结果保存于 {output_file}")
    except subprocess.CalledProcessError as e:
        print("cloc 执行失败:", e)

# 读取 JSON 并绘图
def plot_cloc_results(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 'header' in data:
        data.pop('header')  # 移除非语言部分
    if 'SUM' in data:
        data.pop('SUM')     # 可选：移除总计部分

    languages = list(data.keys())
    code_lines = [data[lang]['code'] for lang in languages]

    plt.figure(figsize=(10, 6))
    plt.barh(languages, code_lines, color='skyblue')
    plt.xlabel('代码行数')
    plt.title('Unity 项目各语言代码行数统计')
    plt.tight_layout()
    plt.show()

# 主执行逻辑
if __name__ == "__main__":
    run_cloc(UNITY_PROJECT_PATH)
    plot_cloc_results("cloc_output.json")
