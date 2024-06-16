import base64
import requests
import os
import time

# 遍历某个文件夹下所有图片
def query_picture(dir_path):
    pic_path_list = []
    for filename in os.listdir(dir_path):
        pic_path_list.append(dir_path + filename)
    return pic_path_list

def extract_table_header(words_list):
    for word in words_list:
        if "表" in word: # 自定义提取方法
            return word
    return None

pic_dir = "./source/"
if __name__ == '__main__':
    pic_list = query_picture(pic_dir)
    if len(pic_list) > 0:
        for i in pic_list:
            print(i) # 打印路径
            url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
            access_token = '' # 获取token
            request_url = url + "?access_token=" + access_token

            f = open(i, 'rb')
            payload = {'image': base64.b64encode(f.read())}
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.post(request_url, data=payload, headers=headers)
            f.close()

            if response:
                # 处理 OCR 结果
                result = response.json()
                words_list = []
                if 'words_result' in result:
                    if len(result['words_result']) > 0:
                        for w in result['words_result']:
                            words_list.append(w['words'])
                        print(words_list)
                        file_name = extract_table_header(words_list)  # 提取表格行头作为文件名
                        if file_name == None:
                            file_name = 'None' + '-' + str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
                        else:
                            file_name += str(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
                        print("file name: " + file_name)
                        os.rename(i, pic_dir + str(file_name).replace("/", "") + '.jpg')
            else:
                print("Error: Failed to send POST request")