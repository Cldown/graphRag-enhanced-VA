import json
import os
import subprocess

from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

@app.route('/datas', methods=['POST'])
def post_data():
    # 检查是否有文件上传
    if 'file' not in request.files:
        return jsonify({'code': 500, 'msg': 'No file part in the request'})

    file = request.files['file']  # 获取上传的文件

    # 检查文件名是否有效且为 CSV 文件
    if file.filename == '' or not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() == 'csv'):
        return jsonify({'code': 500, 'msg': 'Invalid file format. Please upload a CSV file.'})

    # 保存文件到指定路径
    save_path = './feature/feature_extraction/features/user_input.csv'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # 创建目录（如果不存在）
    file.save(save_path)

    try:
        # 调用 Python 脚本处理文件
        subprocess.run(['python', 'final/feature_pipe.py'], check=True)
        return jsonify({'code': 200, 'msg': 'File processed successfully.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'code': 500, 'msg': f'Error running feature_pipe.py: {str(e)}'})
    

# json格式：
#{
#   "order": "qert"
#}
@app.route('/orders', methods=['POST'])
def post_orders():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    order = json_data['order'] #请求
    print(order)
    image_path = './this.png'
    return send_file(image_path, mimetype='image/png'), 200


if __name__ == '__main__':
    app.run(debug=True, host = 'localhost',port=8088)