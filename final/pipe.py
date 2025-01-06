import subprocess
import os
import tempfile
import get_Image as trans
# 读取txt文件内容并转换为字符串
def read_file_as_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()  # 读取整个文件内容
    return file_content


def modify_first_line_and_append(file_path, new_first_line, text_to_append):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 修改第一行
    lines[0] = new_first_line + '\n'

    # 将文件内容重新写入，修改后的内容
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

    # 在文件末尾添加新的一行
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write('\n' + text_to_append + '\n')





# 执行命令
def run_pipe(question):
    # 设置工作目录
    working_directory = r"E:\GraphRag\graphrag"

    # 激活的环境路径
    environment_name = "graphrag-py3.11"
    query_file = r"E:\GraphRag\graphrag\final\field_features.txt"
    new_first_line = " My data set has the following characteristics, What type do you think I should use to visualize the data : "
    # new_first_line = "Analyze the following data"
    text_to_append = ""
    modify_first_line_and_append(query_file, new_first_line, text_to_append)
    file_content = read_file_as_string(query_file)

    # 创建一个临时文件并写入内容
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name  # 临时文件的路径
    # 定义命令，直接使用 temp_file_path
    command = [
        "graphrag",
        "query",
        "--root", "./final",
        "--method", "global",
        "--query", f"@{temp_file_path}"  # 使用临时文件路径
    ]

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

    # 删除临时文件
    os.remove(temp_file_path)
    type = trans.get_type()
    data = trans.csv_to_string("../feature/feature_extraction/features/user_input.csv")
    trans.get_image(type,data,question)
    trans.get_response(question)


question = "Layers大于12000的国家有哪些"
run_pipe(question)
