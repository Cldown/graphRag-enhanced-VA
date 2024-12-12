import subprocess
import os

# 定义命令
command = [
    "graphrag",
    "query",
    "--root", "./final",
    "--method", "global",
    "--query",
    """
    My data has the following characteristics:
    data_type is string. 
    What type do you think I should use for visualization
    """
]

# 设置工作目录
working_directory = r"E:\GraphRag\graphrag"

# 激活的环境路径
environment_name = "graphrag-py3.11"

# 执行命令
try:
    result = subprocess.run(
        command,
        cwd=working_directory,  # 切换到 graphrag 所需的目录
        capture_output=True,  # 捕获命令输出
        text=True,  # 输出作为文本处理
        shell=True,  # 使用 shell 模式支持激活环境命令
        check=True  # 非零退出码会引发异常
    )

    print(result.stdout)

    # 保存输出到文件
    output_file = os.path.join(working_directory, "./final/output.txt")
    with open(output_file, "w") as file:
        file.write(result.stdout)
        print(f"Output saved to {output_file}")

except subprocess.CalledProcessError as e:
    # 捕获执行错误
    print("Error occurred while executing the command:")
    print(e.stderr)
