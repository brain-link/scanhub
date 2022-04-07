# import unittest

# import azure.functions as func
# from my_second_function import main

# class TestFunction(unittest.TestCase):
#     def test_http_request_function(self):
#         # Construct a mock HTTP request.
#         req = func.HttpRequest(
#             method='GET',
#             body=None,
#             url='/api/my_second_function',
#             params={'value': '21'})

#         # Call the function.
#         resp = main(req)

#         # Check the output.
#         self.assertEqual(
#             resp.get_body(),
#             b'21 * 2 = 42',
#         )


import requests
from requests.structures import CaseInsensitiveDict

url = "http://localhost:81/api/TriggerProcessing"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
data = '{ "senderID": 123456, "documentList": ["sample_file1.txt", "sample_file2.txt", "sample_file3.txt", "sample_file4.txt", "sample_file5.txt"] }'

resp = requests.post(url, headers=headers, data=data)

print(resp.status_code)
