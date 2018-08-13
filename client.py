from vps_common_functions import *

# Main Program
#captured_image_filename = getRaspberryPiImage()
captured_image_filename="rose.jpg"
# this is done for testing purpose from swiss alps
client_config_data_json = readConfigFile("client")
file_info = client_config_data_json['image_info']['test_image_url'] + captured_image_filename
print (client_config_data_json['image_info']['test_image_url'])
print (captured_image_filename)
print (file_info)
encoded_data_for_transmission = encodeFile(file_info)
answer=send_PUT_API(encoded_data_for_transmission, client_config_data_json['http_info']['http_connection_socket'])
