import json
import os
import shutil

def mult_rids(rids):
    rids = rids.replace(" ", "")
    rids = rids.split(",")
    dic = {}
    rids = dic.fromkeys(rids).keys()
    rids = list(rids)
    return rids

# 加载config.json
def load_conf(config_copy):
    config_url = os.path.dirname(os.path.realpath(__file__)) + '\\config.json'
    try:
        f = open(config_url, "r")
        conf = json.loads(f.read())
        config_copy = conf.copy()
        f.close()
    except:
        print("config.json不存在或无法读取文件，请重新获取。")
    return config_copy

# 修改config.json个别项
class modify_conf():
    def __init__(self, item, value):
        self.item = item
        self.value = value
        self.bak_conf()
        self.tran_str()
        self.modify_key_value()
    
    def bak_conf(self):
        conf_path = os.getcwd() + '/config.json'
        if os.path.exists(conf_path) and not os.path.exists(conf_path+".bak"):
            shutil.copyfile(conf_path, (conf_path + ".bak"))
            print("\n\rconfig.json已备份。")

    def tran_str(self):
        # 简单判定合法类型
        if type(self.value) == list:
            for i in range(len(self.value)):
                if type(self.value[i])==(int or str):
                    self.value[i] = str(self.value[i])
                else:
                    print("\n\r\033[4;31;43m-> 不支持的类型，仅支持单个int、str或包含int和str的一维简单list。\033[0m",end="")
                    return 0
        elif type(self.value) == int or type(self.value) == str:
            self.value = str(self.value)
        else:
            print("\n\r\033[4;31;43m-> 不支持的类型，仅支持单个int、str或包含int和str的一维简单list。\033[0m",end="")
            return 0

    # 修改config.json的某一项
    def modify_key_value(self):
        config = {}
        config = load_conf(config)
        # 修改键值对
        config[str(self.item)] = str(self.value)  
        # 写入json
        f = open("config.json", 'wt')
        json.dump(config, f, indent=4, ensure_ascii=False)
        f.close()
    
    # 还原config备份
    def restore_conf(self):
        conf_path = os.getcwd() + '/config.json'
        conf_bak_path = conf_path + '.bak'

        if not os.path.exists(conf_bak_path):
            print("\n\r\033[4;31;43m-> config备份不存在。\033[0m",end="")
            return 0

        os.remove(conf_path)
        if os.path.exists(conf_path):print("\n\r\033[4;31;43m-> 恢复config失败，请手动恢复。\033[0m",end="")
        shutil.copyfile(conf_bak_path, conf_path)
        print("\033[7;36m,","\r-> config恢复完成。\033[0m")







