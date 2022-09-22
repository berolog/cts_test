import argparse
from artifactory import ArtifactoryPath
import tarfile, os, sys
import gzip
import xml.etree.ElementTree as ET
from influxdb import InfluxDBClient
from datetime import datetime


parser = argparse.ArgumentParser(description="Just an example",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-a", "--artifactory", help="artifactory url")
parser.add_argument("-i", "--influx", help="influx url")
args = parser.parse_args()
config = vars(args)


artifactory_url = config["artifactory"]
influx_url = config["influx"]

archive = "CTS_16.tgz"
path = ArtifactoryPath(
    artifactory_url,
    auth=("wam_serviceddwdevopssrv", "eyJ2ZXIiOiIyIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYiLCJraWQiOiJYNlUwUC0wblJkNFU4NVNmM0F4TENWelZyU0hpcGtXSGRrM1QwOEtEOXk0In0.eyJleHQiOiJ7XCJyZXZvY2FibGVcIjpcInRydWVcIn0iLCJzdWIiOiJqZmFjQDAxZnJxYnBqbnFkNTUwMXMyc2YzcXAxMHg0XC91c2Vyc1wvd2FtX3NlcnZpY2VkZHdkZXZvcHNzcnYiLCJzY3AiOiJhcHBsaWVkLXBlcm1pc3Npb25zXC9hZG1pbiIsImF1ZCI6IipAKiIsImlzcyI6ImpmZmVAMDAwIiwiZXhwIjoxNjY0ODA2MDAzLCJpYXQiOjE2NTcwMzAwMDMsImp0aSI6IjNhZDhiNmY4LTBhMjAtNGI4YS04YjE1LWFiZjQzNGQwYmYyOSJ9.SwpA7UX4lwNrvC_eTRnaI0_0Ghl4MXsJw08_pUP8x4vmJ5GVFQSdwFktCUifwGTnm5WZBFmR8k1HWoL_RmGJi57ypEGNNjZx2UjTpasF6HhSwoPm4-smP21FD0_wRfoYqKXlnlbe6I3JhSwLdZiWA2LCZpWvpF4R75B-5ERf91mtt5AeCxsV8_3saBVrDgCPzXxBtcjgNbvJvLhdRlhZwBfY_lc8tBLabdoJkD3_rX-BwnMfPBcyN2rGfJhMVCaKaeWe9ghHD8oO1wBnBk0IYPkMuzoGS8oBouNBPmAqBnC_Rgny1JNCiBvId4bKTlqymB-ZIahSaXfpU2wlh0j-CQ"),
)

with path.open() as fd:
    with open(archive, "wb") as out:
        out.write(fd.read())


tar = tarfile.open(archive, 'r:gz')
tar.extractall()


#tree = ET.parse('./android-cts/results/latest/test_result.xml')
#root = tree.getroot()

#client = InfluxDBClient(influx_url, 8086, 'admin', 'GfhjkJhtk1213')

#client.switch_database('cts')

#for summary in root.iter('Summary'):
#    for module in root.iter('Module'):
#        for testCase in module.iter('TestCase'):
#            for test in testCase.iter('Test'):
#                json = [
#                    {
#                        "measurement": "cts",
#                        "tags": {
#                            "module_name": str(module.attrib['name']),
#                            "module_abi": str(module.attrib['abi']),
#                            "pass": str(module.attrib['pass']),
#                            "total_tests": str(module.attrib['total_tests']),
#                            "testCase_name": str(testCase.attrib['name']),
#                            "test_name": str(test.attrib['name']),
#                            "result": str(test.attrib['result']),
#                            "summary_pass": int(summary.attrib['pass']),
#                            "summary_fail": int(summary.attrib['failed']),
#                            "modules_done": int(summary.attrib['modules_done']),
#                            "modules_total": int(summary.attrib['modules_total']),
#                        },
#                        "time": datetime.fromtimestamp(int(root.attrib['end']) / 1000),
#                        "fields": {
#                            "name": "CTS"
#                        }
#                    }
#                ]
                #client.write_points(json)
#                print(json)
