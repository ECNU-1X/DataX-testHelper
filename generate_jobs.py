"""
为了方便测试，自动生成job配置文件

"""

__python__ = 3.6

import json
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
},
{
    "name": "dx_md5",
    "parameter": 
        {
            "columnIndex":1,
            "paras":[""]
        }  
}
]

run_cmd = []
class JobGenerator:
    def __init__(self, json_file_path):
        self.__basic_template = json.loads(open(json_file_path, encoding="utf-8").read())
        self.__basic_template_file = json_file_path
        self.__init_settings = None

    def reset_settings(self):
        self.__basic_template = json.loads(open(self.__basic_template_file, encoding="utf-8").read())

    def get_init_setting(self):
        if __init_settings:
            return self.__init_settings

    def set_writer(self, writer):
        content = self.__basic_template["job"]["content"]
        if not content:
            content.append({"writer":writer})
        else:
            content[0]["writer"] = writer

    def set_reader(self, writer):
        content = self.__basic_template["job"]["content"]
        if not content:
            content.append({"reader":reader})
        else:
            content[0]["reader"] = reader

    def add_transformer(self, transformer):
        content = self.__basic_template["job"]["content"]
        if not content:
            content.append({"transformer":[transformer]})
        else:
            content[0]["transformer"] = [transformer]

    def get_template(self):
        return copy.deepcopy(self.__basic_template)

    def save_template(self, to_file_path):
        with open(to_file_path, "w") as fw:
            fw.write(json.dumps(self.__basic_template))


def generate_jobs(reader, writer, transformer, **paras):
    g = JobGenerator("template_job.json")
    g.set_reader(reader)
    g.set_writer(writer)
    for size in ["1000", "10000", "100000", "1m", "10m", "100m", "1G"]:
        data_file_path = "/root/liukun/%s/*"%size
        path = reader["parameter"]["path"]
        if len(path) == 0:
            path.append(data_file_path)
        else:
            path[0] = data_file_path
        g.set_reader(reader)
        g.add_transformer(transformer)
        transformer_name = transformer["name"]
        if transformer_name == "dx_cryp":
            transformer_name = transformer_name + "-" + transformer["parameter"]["paras"][0]
        new_job_name = transformer_name + size +".json"
        run_cmd.append("python datax.py ../job/%s >> testlog/%s.log\n"%((new_job_name, new_job_name)))
        g.save_template(new_job_name)
    with open("run_test.sh", "w") as fw:
        for cmd in run_cmd:
            fw.write(cmd)

if __name__ == '__main__':
    g = JobGenerator("template_job.json")
    writer = {
                "name": "streamwriter",
                "parameter": 
                {
                    "print": False,
                        "encoding": "UTF-8"
                }
            }
    reader = {      
                "name": "txtfilereader",
                "parameter": {
                    "path": [],
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
            }
    for transformer in transformer_set:
        g.reset_settings()
        g.set_writer(writer)
        g.set_reader(reader)
        g.add_transformer(transformer_set)
        generate_jobs(reader, writer, transformer)
    # import pprint
    # pprint.pprint(g.get_template())
    # g.save_template("RSA_E")