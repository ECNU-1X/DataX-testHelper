"""
为了方便测试，自动生成job配置文件

从txt文件读取数据，处理后的数据不落盘。
"""

import copy
transformer_set = [{
    "name": "dx_enum",
    "parameter": 
        {
            "columnIndex":0,
            "paras":["10"]
        }  
},
{
    "name": "dx_floor",
    "parameter": 
        {
            "columnIndex":0,
            "paras":[""]
        }  
},
{
    "name": "dx_hiding",
    "parameter": 
        {
            "columnIndex":1,
            "paras":[""]
        }  
},                    
{
    "name": "dx_prefix_preserve",
    "parameter": 
        {
            "columnIndex":0,
            "paras":["5"]
        }  
}]

setting_str = """{"setting": {},
    "job": {
        "setting": {
            "speed": {
                "channel": 1
            }
        },
        "content": [
            {
                "reader": {
                    "name": "txtfilereader",
                    "parameter": {
                        "path": ["%s"],
                        "encoding": "UTF-8",
                        "column": [
                            {
                                "index": 0,
                                "type": "long"
                            },
                            {
                                "index": 1,
                                "type": "string"
                            }
                        ],
                        "fieldDelimiter": ","
                    }
                },
                "writer": {
                    "name": "streamwriter",
                    "parameter": {
                        "print": false,
                        "encoding": "UTF-8"
                    }
                },
                "transformer": [
                %s
                ]
            }
        ]
    }
}
"""

run_cmd = []

import json
for s in transformer_set:
    for size in ["1G"]:#["1000", "10000", "100000", "1m", "10m", "100m"]:
        data_file_path = "/root/liukun/%s/*"%size
        setting = setting_str%(data_file_path, json.dumps(s))
        new_job_name = s["name"]+size+".json"
        run_cmd.append("python datax.py ../job/%s >> testlog/%s.log\n"%((new_job_name, new_job_name)))
        with open(new_job_name, "w", encoding="utf-8") as fw:
            fw.write(setting)

with open("run_test.sh", "w") as fw:
    for cmd in run_cmd:
        fw.write(cmd)
