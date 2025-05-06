import os
import re
import matplotlib.pyplot as plt
from collections import defaultdict
import chardet

# === 设置你的 Unity 项目路径 ===
UNITY_PROJECT_PATH = "/Users/vanish/Desktop/DungeonPension/branches/dev_vanish/Assets/Scripts"  # 修改这里


# === 设置 matplotlib 中文显示（macOS / Windows）===
plt.rcParams['font.family'] = 'PingFang SC'  # macOS
# plt.rcParams['font.family'] = 'SimHei'     # Windows 中文字体
plt.rcParams['axes.unicode_minus'] = False

# === 自动检测编码并读取内容 ===
def read_file_safely(filepath):
    with open(filepath, "rb") as f:
        raw = f.read()
        result = chardet.detect(raw)
        encoding = result['encoding'] or 'utf-8'
    try:
        return raw.decode(encoding, errors='replace')
    except Exception as e:
        print(f"⚠️ 读取文件失败: {filepath} ({encoding}) -> {e}")
        return ""

# === 判断有效代码行 ===
def is_code_line(line):
    stripped = line.strip()
    return stripped and not stripped.startswith("//")

# === 提取命名空间 ===
def extract_namespace(content):
    match = re.search(r'namespace\s+([\w\.]+)', content)
    return match.group(1) if match else "无命名空间"

# === 主逻辑：遍历并统计 ===
def analyze_unity_cs_files(project_path):
    file_line_counts = {}
    namespace_line_counts = defaultdict(int)

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".cs"):
                full_path = os.path.join(root, file)
                content = read_file_safely(full_path)
                lines = content.splitlines()
                code_lines = [line for line in lines if is_code_line(line)]
                line_count = len(code_lines)

                file_line_counts[full_path] = line_count

                header = "\n".join(lines[:30])  # 只取前 30 行用于提取命名空间
                ns = extract_namespace(header)
                namespace_line_counts[ns] += line_count

    return file_line_counts, namespace_line_counts

# === 可视化输出 ===
def plot_results(data_dict, title, top_n=15):
    sorted_items = sorted(data_dict.items(), key=lambda x: x[1], reverse=True)[:top_n]
    labels = [os.path.basename(k) if "/" in k else k for k, _ in sorted_items]
    values = [v for _, v in sorted_items]

    plt.figure(figsize=(10, 6))
    plt.barh(labels, values, color='skyblue')
    plt.xlabel("lines")
    plt.title(title)
    plt.gca().invert_yaxis()
    for i, v in enumerate(values):
        plt.text(v + 5, i, str(v), va='center')
    plt.tight_layout()
    plt.show()

# === 执行分析 ===
if __name__ == "__main__":
    files, namespaces = analyze_unity_cs_files(UNITY_PROJECT_PATH)
    print(f"[✓] 共统计 {len(files)} 个 .cs 文件")

    plot_results(files, "Top 15 Files")
    plot_results(namespaces, "Top 15 NameSpaces")
