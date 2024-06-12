import json
import xml.etree.ElementTree as ET
import sys

def json_to_junit(json_data):
    # Create the root element 'testsuites'
    testsuites = ET.Element("testsuites")
    testsuite = ET.SubElement(testsuites, "testsuite", name="Vulnerabilities", tests=str(len(json_data["vulnerabilities"])))
    for index, vulnerability in enumerate(json_data["vulnerabilities"]):
        testcase = ET.SubElement(testsuite, "testcase", classname=vulnerability["category"], name=str(index) + "-" + vulnerability["name"])
        
        failure_text = f"Description: {vulnerability['description']}\n"
        location = vulnerability['location']
        
        start_line = location.get('start_line', 'N/A')
        # Get 'end_line' and provide a default if it does not exist
        end_line = location.get('end_line', start_line)
        
        if 'end_line' in location:
            failure_text += f"File: {location['file']} (Lines {start_line}-{end_line})\n"
        else:
            failure_text += f"File: {location['file']} (Line {start_line})\n"
        
        failure_text += f"Severity: {vulnerability['severity']}\n"
        failure_text += f"Scanner: {vulnerability['scanner']['name']} ({vulnerability['scanner']['id']})\n"
        failure_text += f"CVE: {vulnerability['cve']}\n"
        failure_text += f"Identifiers:\n"
        
        for identifier in vulnerability["identifiers"]:
            failure_text += f"  - {identifier['type']}: {identifier['name']} (Value: {identifier['value']})\n"
            if 'url' in identifier:
                failure_text += f"    URL: {identifier['url']}\n"
        
        ET.SubElement(testcase, "failure", message="Vulnerability detected").text = failure_text

    # Convert the ElementTree to a string
    junit_xml = ET.tostring(testsuites, encoding="utf-8", method="xml").decode("utf-8")

    # Prettify the XML
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(junit_xml)
    pretty_xml_as_string = dom.toprettyxml()

    return pretty_xml_as_string

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python json_to_junit.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    
    # Read and parse the JSON file
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)

    # Convert the file to JUnit.xml
    junit_xml = json_to_junit(json_data)

    # Create the JUnit report
    with open("junit_report.xml", "w") as file:
        file.write(junit_xml)

    print("JUnit XML report has been generated and saved as 'junit_report.xml'.")
    if len(json_data["vulnerabilities"]) > 0:
        print("Vulnerabilities detected. Exiting with status code 1.")
        sys.exit(1)