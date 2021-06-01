# copy data from clipboard to file on unix: 
# xsel --clipboard > ~/map.json
# paste data:
# cat ./df_chunked_1.json | xclip -selection c

import json
import ast

with open('map.json', 'r') as f:
    data = f.read()
    f.close()
data_str = str(data)

def eval_str(str_dict):
    bytes_data = bytes(str_dict.encode())
    dict_str = bytes_data.decode("UTF-8")
    return ast.literal_eval(dict_str)

data_test_str = data[1:-1].replace("\n","")
chunk_list = []
i=0
while data_test_str.find("chunkFootprint") != -1:
    i+=1
    cf = data_test_str.find("chunkFootprint")
    a = data_test_str.find("{")
    b = data_test_str[cf+1:].find("chunkFootprint")
    if b != -1:
#         one_chunk = eval_str(data_test_str[a:cf+1+b-3])
        one_chunk = data_test_str[a:cf+1+b-3]
        chunk_list.append(one_chunk)
        data_test_str = data_test_str[cf+1+b-2:]
        cf=0
        a=0
        b=0
        if i%1000==0:
            print(i,one_chunk)
    else:
#         one_chunk = eval_str(data_test_str[a:])
        one_chunk = data_test_str[a:]
        data_test_str=""
        chunk_list.append(one_chunk)
        print("Chunk list ready, len:",len(chunk_list))
        
chunks_dump = [] 
FILE_CHUNKS_LIMIT = 100 # limit 100 chunks per file
i = 0
f_nr = 1
print("Dumping data to files")
for chunk in chunk_list:
    if i<FILE_CHUNKS_LIMIT:
        i+=1
        chunks_dump.append(chunk)
    else:
        print("Saving",'df_chunked_'+str(f_nr)+'.json')
        i=0
        file = open('df_chunked_'+str(f_nr)+'.json','w')
        chunks_dump_str=""
        for chunk_str in chunks_dump:
            chunks_dump_str+=chunk_str+','
        file.write("["+chunks_dump_str[:-1]+"]")
        file.close()
        chunks_dump = []
        f_nr+=1
if i>0:
    print("Saving",'df_chunked_'+str(f_nr)+'.json')
    i=0
    file = open('df_chunked_'+str(f_nr)+'.json','w')
    chunks_dump_str=""
    for chunk_str in chunks_dump:
        chunks_dump_str+=chunk_str+','
    file.write("["+chunks_dump_str[:-1]+"]")
    file.close()
    chunks_dump = []
    f_nr+=1
print("DONE!")
