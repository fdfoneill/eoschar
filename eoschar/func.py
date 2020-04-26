import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import json

def getModel(file_name):
	modelFile = os.path.join(os.path.dirname(os.path.dirname(__file__)),"resources",file_name)
	with open(modelFile,'r') as rf:
		return json.loads(rf.read().replace('/u2019',"'"))

def getYesNo(message:str) -> bool:
	response = input(message+"\n[Y/N]: ")
	if response.lower() in ["y","yes"]:
		return True
	elif response.lower() in ['n','no']:
		return False
	else:
		log.warning(f"Expected Y or N; got {response}")
		getYesNo(message)

def clearScreen(): 
  
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear')