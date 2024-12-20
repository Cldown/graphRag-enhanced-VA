import subprocess
import os

# 定义路径
working_directory = r"D:\AAAcourse\3\1-大三上\科研课堂-软件智能可视化\project\graphrag-va\graphrag-enhanced-VA"  # 根目录
script_to_run = os.path.join(working_directory, "feature/feature_extraction/features/my_single_field_features.py")
output_file = os.path.join(working_directory, "./final/field_features.txt")  # 输出文件路径

try:
    # 调用 my_single_field_features.py 并捕获其输出，指定 utf-8 编码
    result = subprocess.run(
        ["python", script_to_run],  # 调用目标脚本
        cwd=working_directory,  # 设置工作目录
        capture_output=True,  # 捕获输出
        text=True,  # 以文本形式处理输出
        encoding='utf-8',  # 显式设置编码
        check=True  # 如果非零退出码则引发异常
    )

    # 获取标准输出
    output_str = result.stdout.strip()

    # 打印供调试
    # print("Captured output_str:", output_str)

    # 将输出写入文件，让 pipe.py 使用
    with open(output_file, "w") as file:
        file.write(output_str)
        print(f"Output saved to {output_file}")

except subprocess.CalledProcessError as e:
    # 捕获运行错误并打印
    print("Error occurred while executing my_single_field_features.py:")
    print(e.stderr)

except UnicodeDecodeError as e:
    print(f"Unicode decoding error: {e}")
