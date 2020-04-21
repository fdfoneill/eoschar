import logging, os
logging.basicConfig(level=os.environ.get("LOGLEVEL","INFO"))
log = logging.getLogger(__name__)

import json

def getModel(file_name):
	modelFile = os.path.join(os.path.dirname(os.path.dirname(__file__)),"resources",file_name)
	with open(modelFile,'r') as rf:
		return json.loads(rf.read())