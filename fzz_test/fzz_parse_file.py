from serpapi import google_scholar_search
import os
import requests

# openai_key = input("please input openai key: ")
# print(openai_key)
dict_format = {
    "PDF": '.pdf'
}

MAX_NUM = 20

def parse_orig_json(organic_results):
    res_list = []
    for i in organic_results:
        tmp_res = {}
        tmp_res['title'] = i['title']
        tmp_res['link'] = i['resources'][0]['link']
        tmp_res['format'] = dict_format[i['resources'][0]['file_format']]
        tmp_res['pos'] = i['position']
        tmp_res['id'] = i['result_id']
        tmp_res['file_name'] = "./data/scholar_corpus/" + tmp_res['id'] + tmp_res['format']
        res_list.append(tmp_res)
    fin = open("./data/scholar_corpus/dict.txt")
    cur_dict_str = fin.read()
    fin.close()
    # print(cur_dict_str)
    cur_dict = None
    if(cur_dict_str != ""):
        cur_dict = eval(cur_dict_str)
    else:
        cur_dict = {}
    
    for i in res_list:
        if(i['id'] not in i.keys()):
            cur_dict[i['id']] = i
            cur_url = i['link']
            response = requests.get(cur_url)
            file_name = i['file_name']
            with open(file_name, "wb") as file:
                file.write(response.content)
    fout = open("./data/scholar_corpus/dict.txt", "w+")
    fout.write(str(cur_dict))
    fout.close()
    return cur_dict

def scholar_search(search_num=10, cites=None, query=None):
    if((cites == None and query == None) or search_num < 1):
        print("invalid param")
        return
    # if(search_num > MAX_NUM):
    tmp_num = search_num
    start = 0
    while tmp_num > 0:
        cur_num = tmp_num
        if(tmp_num > MAX_NUM):
            cur_num = MAX_NUM
        search = None
        if(cites == None):
            search = google_scholar_search.GoogleScholarSearch({##其实还可以加上q，但是不重要，以后可以再加上
                "q": query, 
                "api_key": api_key,
                "start": start,
                "num": cur_num
            })
        else:
            search = google_scholar_search.GoogleScholarSearch({##其实还可以加上q，但是不重要，以后可以再加上
                "cites": cites, 
                "api_key": api_key,
                "start": start,
                "num": cur_num
            })
        result = search.get_dict()
        organic_results = result['organic_results']
        cur_dict = parse_orig_json(organic_results)
        tmp_num -= cur_num
        start += cur_num
    return cur_dict


api_key = os.getenv("serp_api_key")
api_key = input("please input serp_api_key: ")
print(api_key)

mode = input("normal search 1;document reference 0; default 1:")

res_dict = {}

search_num = eval(input("search num: "))
if(mode == '0'):##直接使用文档索引来搜索
    doc_id = input("input docid: ")
    cur_dict = scholar_search(search_num, doc_id, None)
else:##直接使用搜索词搜索
    query = input("query: ")
    cur_dict = scholar_search(search_num, None, query)
