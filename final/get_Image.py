import json
from zhipuai import ZhipuAI
import altair as alt
import base64
stack_vega = """
{
  "data": {
    "values": [
      {"x": 1, "column1": 10, "column2": 20},
      {"x": 2, "column1": 15, "column2": 25},
      {"x": 3, "column1": 20, "column2": 30}
    ]
  },
  "mark": "bar",
  "encoding": {
    "x": {"field": "x", "type": "quantitative", "sort":null},
    "y": {"field": "value", "type": "quantitative"},
    "color": {"field": "column", "type": "nominal"}
  },
  "transform": [
    {
      "fold": ["column1", "column2"],
      "as": ["column", "value"]
    }
  ]
}

"""

coloums_vega= """
{
  "data": {
    "values": [
      {"x": 1, "column1": 10, "column2": 20},
      {"x": 2, "column1": 15, "column2": 25},
      {"x": 3, "column1": 20, "column2": 30}
    ]
  },
  "transform": [
    {
      "fold": ["column1", "column2"],
      "as": ["column", "value"]
    }
  ],
  "mark": "bar",
  "encoding": {
    "x": {
      "field": "x",
      "type": "ordinal",  
      "sort":null
    },
    "y": {
      "field": "value",
      "type": "quantitative"
    },
    "color": {
      "field": "column",
      "type": "nominal"
    },
    "xOffset": {
      "field": "column",
      "type": "nominal",
      "scale": {
        "domain": ["column1", "column2"],
      }
    }
  }
}

"""
line_vega="""
{
  "data": {
    "values": [
      {"Year": 2018, "Number of Tourists": 7000, "Hotel Revenue": 500, "Restaurant Revenue": 800},
      {"Year": 2019, "Number of Tourists": 9000, "Hotel Revenue": 550, "Restaurant Revenue": 900},
      {"Year": 2020, "Number of Tourists": 10000, "Hotel Revenue": 600, "Restaurant Revenue": 1000},
      {"Year": 2021, "Number of Tourists": 8000, "Hotel Revenue": 650, "Restaurant Revenue": 1100},
      {"Year": 2022, "Number of Tourists": 9500, "Hotel Revenue": 700, "Restaurant Revenue": 1200}
    ]
  },
  "transform": [
    {
      "fold": ["Hotel Revenue", "Restaurant Revenue"],
      "as": ["Revenue Type", "Revenue"]
    }
  ],
  "mark": "line",
  "encoding": {
    "x": {
      "field": "Year",
      "type": "quantitative",
      "sort":null
    },
    "y": {
      "field": "Revenue",
      "type": "quantitative"
    },
    "color": {
      "field": "Revenue Type",
      "type": "nominal"
    },
    "tooltip": [
      {"field": "Year", "type": "quantitative"},
      {"field": "Revenue", "type": "quantitative"},
      {"field": "Revenue Type", "type": "nominal"}
    ]
  }
}
"""
box_vega="""
{
  "data": {
    "values": [
      {"Retail Store": "Department Store", "Min": 20, "Q1": 50, "Median": 80, "Q3": 110, "Max": 150, "Outlier": []},
      {"Retail Store": "Shopping Mall", "Min": 15, "Q1": 40, "Median": 65, "Q3": 90, "Max": 120, "Outlier": [200]},
      {"Retail Store": "Grocery Store", "Min": 10, "Q1": 30, "Median": 50, "Q3": 70, "Max": 100, "Outlier": [150, 300]},
      {"Retail Store": "Online Store", "Min": 5, "Q1": 25, "Median": 45, "Q3": 65, "Max": 85, "Outlier": [95, 110]},
      {"Retail Store": "Discount Store", "Min": 25, "Q1": 60, "Median": 75, "Q3": 90, "Max": 105, "Outlier": [120, 150]}
    ]
  },
  "layer": [
    {
      "mark": "boxplot",
      "encoding": {
        "x": {
          "field": "Retail Store",
          "type": "nominal",
          "axis": {
            "title": "Retail Store"
          },
          "sort":null
        },
        "y": {
          "field": "Value",
          "type": "quantitative",
          "axis": {
            "title": "Value"
          }
        },
        "color": {
          "field": "Retail Store",
          "type": "nominal"
        }
      },
      "transform": [
        {
          "fold": ["Min", "Q1", "Median", "Q3", "Max"],
          "as": ["Stat", "Value"]
        }
      ]
    },
    {
      "mark": "point",
      "encoding": {
        "x": {
          "field": "Retail Store",
          "type": "nominal"
        },
        "y": {
          "field": "Outlier",
          "type": "quantitative"
        },
        "color": {
          "field": "Retail Store",
          "type": "nominal"
        }
      },
      "transform": [
        {
          "flatten": ["Outlier"],
          "as": ["Outlier"]
        }
      ]
    }
  ]
}
"""
heatmap_vega="""
{
  "data": {
    "values": [
      {"Region": "North America", "Transport": "Truck", "Count": 500},
      {"Region": "North America", "Transport": "Train", "Count": 250},
      {"Region": "North America", "Transport": "Ship", "Count": 300},
      {"Region": "North America", "Transport": "Plane", "Count": 400},
      {"Region": "North America", "Transport": "Pipeline", "Count": 200},
      {"Region": "South America", "Transport": "Truck", "Count": 200},
      {"Region": "South America", "Transport": "Train", "Count": 150},
      {"Region": "South America", "Transport": "Ship", "Count": 100},
      {"Region": "South America", "Transport": "Plane", "Count": 100},
      {"Region": "South America", "Transport": "Pipeline", "Count": 50},
      {"Region": "Europe", "Transport": "Truck", "Count": 300},
      {"Region": "Europe", "Transport": "Train", "Count": 400},
      {"Region": "Europe", "Transport": "Ship", "Count": 250},
      {"Region": "Europe", "Transport": "Plane", "Count": 200},
      {"Region": "Europe", "Transport": "Pipeline", "Count": 150},
      {"Region": "Asia", "Transport": "Truck", "Count": 1000},
      {"Region": "Asia", "Transport": "Train", "Count": 800},
      {"Region": "Asia", "Transport": "Ship", "Count": 500},
      {"Region": "Asia", "Transport": "Plane", "Count": 1200},
      {"Region": "Asia", "Transport": "Pipeline", "Count": 600},
      {"Region": "Africa", "Transport": "Truck", "Count": 100},
      {"Region": "Africa", "Transport": "Train", "Count": 50},
      {"Region": "Africa", "Transport": "Ship", "Count": 25},
      {"Region": "Africa", "Transport": "Plane", "Count": 50},
      {"Region": "Africa", "Transport": "Pipeline", "Count": 20},
      {"Region": "Australia", "Transport": "Truck", "Count": 300},
      {"Region": "Australia", "Transport": "Train", "Count": 200},
      {"Region": "Australia", "Transport": "Ship", "Count": 100},
      {"Region": "Australia", "Transport": "Plane", "Count": 150},
      {"Region": "Australia", "Transport": "Pipeline", "Count": 75}
    ]
  },
  "mark": "rect",
  "encoding": {
    "x": {
      "field": "Region",
      "type": "nominal",
      "axis": {"title": "Region"},
      "sort":null
    },
    "y": {
      "field": "Transport",
      "type": "nominal",
      "axis": {"title": "Transport Type"}
    },
    "color": {
      "field": "Count",
      "type": "quantitative",
      "legend": {"title": "Count"}
    }
  }
}
"""
histogram_vega = """
{
  "data": {
    "values": [
      {"Range": "0-5", "Count": 14},
      {"Range": "5-10", "Count": 22},
      {"Range": "10-15", "Count": 19},
      {"Range": "15-20", "Count": 13},
      {"Range": "20-25", "Count": 9},
      {"Range": "25-30", "Count": 7},
      {"Range": "30-35", "Count": 5},
      {"Range": "35-40", "Count": 3},
      {"Range": "40-45", "Count": 2},
      {"Range": "45-50", "Count": 1}
    ]
  },
  "mark": "bar",
  "encoding": {
    "x": {
      "field": "Range",
      "type": "nominal",
      "axis": {
        "title": "Gallery Visitors (Thousands)",
        "labelAngle": 45
      },
      "sort": null 
    },
    "y": {
      "field": "Count",
      "type": "quantitative",
      "axis": {
        "title": "Number of Galleries"
      }
    },
    "color": {
      "field": "Range",
      "type": "nominal",
      "legend": {
        "title": "Visitors Range"
      }
    }
  }
}
"""
scatter_vega="""
{
  "data": {
    "values": [
      {"Category": "A", "X": 10, "Y": 20},
      {"Category": "B", "X": 15, "Y": 30},
      {"Category": "A", "X": 20, "Y": 35},
      {"Category": "C", "X": 25, "Y": 40},
      {"Category": "B", "X": 30, "Y": 50},
      {"Category": "C", "X": 35, "Y": 60},
      {"Category": "A", "X": 40, "Y": 80},
      {"Category": "B", "X": 45, "Y": 85},
      {"Category": "C", "X": 50, "Y": 100}
    ]
  },
  "mark": "point",
  "encoding": {
    "x": {
      "field": "X",
      "type": "quantitative",
      "axis": {
        "title": "X Axis (Value)"
      }
    },
    "y": {
      "field": "Y",
      "type": "quantitative",
      "axis": {
        "title": "Y Axis (Value)"
      }
    },
    "color": {
      "field": "Category",
      "type": "nominal",
      "legend": {
        "title": "Category"
      }
    }
  }
}
"""
def get_image(type, data,question):
    client = ZhipuAI(api_key="a939104d5a999a9b68fdcfa4e651356b.wmgjEahqOumFPwol")  # 请填写您自己的APIKey
    # message = 'Please summarize below message data into a Vega-Lite, the trace_type is {}, Do not add other sentences.I wanted to be able to present all the data in a visual way. Data:{}'.format(
    #     type, data)
    chart_type = type.lower()
    if chart_type == "bar":
        requirement = """
        - 图表类型为Bar，你需要注意以下问题：可能会出现一个x变量对应多个数据，此时你需从数据之间的关系来判断使用堆叠方式还是分开多列显示，但一定要保证所有数据能够显示出来，
            - 若使用堆叠方式，可参考以下代码：
                {}
            - 若使用分开多列显示，可参考以下代码：
                {}
            - 需要注意，不要对x轴的数据进行排序，即在encoding的x轴的字段设置"sort"为null，如果x轴的对应显示值太长，可以考虑对x轴的标签的进行旋转，即在encoding的x轴的字段的axis字段设置"labelAngle"为45
        """.format( stack_vega, coloums_vega)
    elif chart_type == "line":
        requirement = """
        图表类型为line，可参考以下代码：
            {}
        """.format(box_vega)
    elif chart_type == "heatmap":
        requirement = """
        - 图表类型为heatmap，可参考以下代码：
            {}
        - 需要注意，不要对x轴的数据进行排序，即在encoding的x轴的字段设置"sort"为null，如果x轴的对应显示值太长，可以考虑对x轴的标签的进行旋转，即在encoding的x轴的字段的axis字段设置"labelAngle"为45
        """.format(heatmap_vega)
    elif chart_type == "histogram":
        requirement = """
        - 图表类型为histogram，可参考以下代码：
            {}
        - 需要注意，不要对x轴的数据进行排序，即在encoding的x轴的字段设置"sort"为null，如果x轴的对应显示值太长，可以考虑对x轴的标签的进行旋转，即在encoding的x轴的字段的axis字段设置"labelAngle"为45
        """.format(histogram_vega)
    elif chart_type == "box":
        requirement = """
        - 图表类型为box，可参考以下代码：
            {}
        - 需要注意，不要对x轴的数据进行排序，即在encoding的x轴的字段设置"sort"为null，
        """.format(box_vega)
    elif chart_type == "scatter":
        requirement = """
        - 图表类型为scatter，可参考以下代码：
            {}
        """.format(scatter_vega)
    else:
        requirement = ""
    message = """
    你是一个数据可视化专家，擅长使用 Vega-Lite 生成清晰和正确的图表。给定以下数据和可视化需求，请编写对应的 Vega-Lite 代码。

    - 数据内容：{}

    - 图表类型：{}
    
    - 可视化需求：
        {}
    请根据这些数据内容、图表类型以及可视化需求，生成对应的 Vega-Lite 代码。确保代码结构简洁，并能清晰地表达数据关系。注意：除了Vega-Lite代码以外，不要添加任何句子
    """.format(data, chart_type,requirement)
    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=[{"role": "user", "content": message}],
    )

    # 获取返回的 Vega-Lite 配置
    vega_lite_spec = response.choices[0].message.content  # 直接访问 content 属性
    filter(vega_lite_spec,question)
    # 由于返回的是字符串格式的 JSON，需要去掉三重反引号并解析 JSON
    try:
        # 去掉返回的三重反引号
        vega_lite_spec = vega_lite_spec.strip('```json\n').strip('\n```')
        # 解析 JSON
        vega_lite_json = json.loads(vega_lite_spec)
    except json.JSONDecodeError as e:
        print("Error decoding Vega-Lite JSON:", e)
        return
    vega_lite_spec = json.loads(vega_lite_spec)
    chart = alt.Chart.from_dict(vega_lite_spec)
    chart.save("output.png")

def csv_to_string(file_path):
    """
    读取本地CSV文件，并将其转义为字符串。

    :param file_path: CSV文件路径
    :return: CSV内容字符串
    """
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_content = file.read()  # 读取文件内容
            return csv_content
    except FileNotFoundError:
        return f"文件 {file_path} 未找到"
    except Exception as e:
        return str(e)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
def get_response(question):
    image_path = "output_filter.png"
    image_base64 = encode_image_to_base64(image_path)
    client = ZhipuAI(api_key="a939104d5a999a9b68fdcfa4e651356b.wmgjEahqOumFPwol")  # 请填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4v",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_base64  # 使用 Base64 编码传递图片
                        }
                    }
                ]
            }
        ]
    )
    print(response.choices[0].message)
def filter(code,question):
    client = ZhipuAI(api_key="a939104d5a999a9b68fdcfa4e651356b.wmgjEahqOumFPwol")
    message = """
    请聚焦于问题所需要展现的数据，对以下Vega-lite代码进行修改(使用Vega-Lite的对应Transform操作），如果没有针对该问题不需要添加任何过滤的条件，返回原代码即可，注意：不要添加除了Vega-lite代码以外的任何句子。
    question:
    {}
    code:
    {}
    """.format(question,code)
    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=[{"role": "user", "content": message}],
    )
    vega_lite_spec = response.choices[0].message.content  # 直接访问 content 属性
    try:
        # 去掉返回的三重反引号
        vega_lite_spec = vega_lite_spec.strip('```json\n').strip('\n```')
        # 解析 JSON
        vega_lite_json = json.loads(vega_lite_spec)
    except json.JSONDecodeError as e:
        print("Error decoding Vega-Lite JSON:", e)
        return
    vega_lite_spec = json.loads(vega_lite_spec)
    chart = alt.Chart.from_dict(vega_lite_spec)
    chart.save("output_filter.png")
def get_type():
    client = ZhipuAI(api_key="a939104d5a999a9b68fdcfa4e651356b.wmgjEahqOumFPwol")
    with open('output.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    message = """
        总结以下报告，从"bar, line, heatmap, histogram, box, scatter"中得到最推荐的可视化类型，注意:只允许生成一个类型，不要添加其他任何内容
        {}
        """.format(text)
    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=[{"role": "user", "content": message}],
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content  # 直接访问 content 属性

# image_path="output.png"
# question="筛选一下Layers大于12000的数据"
# get_response(question)
# file_path = "./userInput/bar_2.csv"  # 替换为实际文件路径
# data = csv_to_string(file_path)
# type = "bar"
# get_image(type, data)
