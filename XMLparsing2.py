import argparse
import xml.etree.ElementTree as ET
from influxdb import InfluxDBClient
from datetime import datetime


parser = argparse.ArgumentParser(description="Parameters",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--influx", help="influx [url:port]")
parser.add_argument("-r", "--report", help="path to test results")
args = parser.parse_args()
config = vars(args)

influx_url = config["influx"].split("http://")[1].split(":")[0]
influx_port = config["influx"].split(":")[2]
report = config["report"]

tree = ET.parse(report)
root = tree.getroot()

client = InfluxDBClient(influx_url, influx_port, database='cts')

for summary in root.iter('Summary'):
    for module in root.iter('Module'):
        for testCase in module.iter('TestCase'):
            for test in testCase.iter('Test'):
                json = [
                    {
                        "measurement": "cts",
                        "tags": {
                            "module_name": str(module.attrib['name']),
                            "module_abi": str(module.attrib['abi']),
                            "pass": str(module.attrib['pass']),
                            "total_tests": str(module.attrib['total_tests']),
                            "testCase_name": str(testCase.attrib['name']),
                            "test_name": str(test.attrib['name']),
                            "result": str(test.attrib['result']),
                            "summary_pass": int(summary.attrib['pass']),
                            "summary_fail": int(summary.attrib['failed']),
                            "modules_done": int(summary.attrib['modules_done']),
                            "modules_total": int(summary.attrib['modules_total']),
                        },
                        "time": datetime.fromtimestamp(int(root.attrib['end']) / 1000),
                        "fields": {
                            "name": report
                        }
                    }
                ]
                client.write_points(json)

