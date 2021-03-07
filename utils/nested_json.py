import json
# https://stackoverflow.com/questions/39233973/get-all-keys-of-a-nested-dictionary/39234154#39234154

file = ''
with open('../samples/fileswithsecrets/huawei.postman_environment.json', 'r') as jsonfile:
    jsonobj = json.load(jsonfile)


def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value)
        else:
            yield (key, value)


def kvpairs(jsonobj):
    if isinstance(jsonobj, dict):
        for key, value in recursive_items(jsonobj):
            if type(value) is list:
                for item in value:
                    if type(item) == dict:
                        for key, value in recursive_items(item):
                            print('{}={}'.format(key, value))
            else:
                print('{}={}'.format(key, value))
    if isinstance(jsonobj, list):
        print("listed json")
        for d in jsonobj:
            for key, value in recursive_items(d):
                if type(value) is list:
                    for i in value:
                        if type(i) == dict:
                            for key, value in recursive_items(i):
                                print('{}={}'.format(key, value))
                else:
                    print('{}={}'.format(key, value))

kvpairs(jsonobj)
