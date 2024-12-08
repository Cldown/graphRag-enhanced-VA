import json
from zhipuai import ZhipuAI

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
    "x": {"field": "x", "type": "quantitative"},
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
      "type": "ordinal"  
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
      "type": "quantitative"
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
          }
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
def get_final_messages(type, data):
    client = ZhipuAI(api_key="a939104d5a999a9b68fdcfa4e651356b.wmgjEahqOumFPwol")  # 请填写您自己的APIKey
    # message = 'Please summarize below message data into a Vega-Lite, the trace_type is {}, Do not add other sentences.I wanted to be able to present all the data in a visual way. Data:{}'.format(
    #     type, data)
    message = """
    你是一个数据可视化专家，擅长使用 Vega-Lite 生成清晰和正确的图表。给定以下数据和可视化需求，请编写对应的 Vega-Lite 代码。

    - 数据内容：{}

    - 图表类型：{}
    
    - 可视化需求：
        - 如果图表类型为Bar，你需要注意以下问题：可能会出现一个x变量对应多个数据，此时你需自己判断使用堆叠方式还是分开多列显示，但一定要保证所有数据能够显示出来，
            - 若使用堆叠方式，可参考以下代码：
                {}
            - 若使用分开多列显示，可参考以下代码：
                {}
        - 如果图表类型为line，可参考以下代码：
                {}
        - 如果图表类型为box，可参考以下代码：
                {}
        - 如果图表类型不属于上述所提供的，请忽略可视化需求，直接生成代码
    请根据这些数据内容、图表类型以及可视化需求，生成对应的 Vega-Lite 代码。确保代码结构简洁，并能清晰地表达数据关系。注意：除了Vega-Lite代码以外，不要添加任何句子
    """.format(data, type, stack_vega, coloums_vega,line_vega,box_vega)
    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=[{"role": "user", "content": message}],
    )

    # 获取返回的 Vega-Lite 配置
    vega_lite_spec = response.choices[0].message.content  # 直接访问 content 属性

    # 由于返回的是字符串格式的 JSON，需要去掉三重反引号并解析 JSON
    try:
        # 去掉返回的三重反引号
        vega_lite_spec = vega_lite_spec.strip('```json\n').strip('\n```')
        # 解析 JSON
        vega_lite_json = json.loads(vega_lite_spec)
    except json.JSONDecodeError as e:
        print("Error decoding Vega-Lite JSON:", e)
        return
    print(vega_lite_spec)
    # 使用 Altair 渲染图表
    # try:
    #     chart = alt.Chart.from_dict(vega_lite_json)
    #     # 保存为图片
    #     chart.save('area_chart.png', scale_factor=3.0)  # 可以调整 scale_factor 来控制图片的清晰度
    #     print("Chart saved as 'area_chart.png'")
    # except Exception as e:
    #     print("Error rendering chart:", e)
    #




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



file_path = "./userInput/box_3.csv"  # 替换为实际文件路径
data = csv_to_string(file_path)
type = "box"
get_final_messages(type, data)
