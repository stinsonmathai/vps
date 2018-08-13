import falcon
from vps_common_functions import *

mecapi = falcon.API()
mecapi.add_route("/test", RequestClass())


#Rohits files paths:
#mod_file = "C:\\Coding\\ML\\tensorflow-for-poets-2-master\\output\\retrained_graph.pb"
#lab_file = "C:\\Coding\\ML\\tensorflow-for-poets-2-master\\output\\retrained_labels.txt"
# mod_file = "/Users/stinsonmathai/programming/machineLearning/tensorflow-for-poets-2/outputs/retrained_graph.pb"
# lab_file = "/Users/stinsonmathai/programming/machineLearning/tensorflow-for-poets-2/outputs/retrained_label.txt"