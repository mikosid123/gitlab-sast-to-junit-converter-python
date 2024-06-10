import json
import xml.etree.ElementTree as ET
import sys

def create_junit_report(json_data, output_file='junit_report.xml'):
    # Create the root element for the JUnit report
    testsuites = ET.Element("testsuites")
    testsuite = ET.SubElement(testsuites, "testsuite", name="TestSuite", tests=str(len(json_data)), failures=str(len(json_data)))

    # Loop through each entry in the JSON data
    for index, test_case in enumerate(json_data):
        # Extract test case information (you can adjust these based on your JSON structure)
        test_name = test_case.get("testName", f"Test-{index}")
        failure_message = test_case.get("message", "No failure message provided")
        
        # Create a test case element
        testcase = ET.SubElement(testsuite, "testcase", name=test_name, classname=test_case.get("classname", "DefaultClass"))

        # Add a failure element to the test case
        failure = ET.SubElement(testcase, "failure", message=failure_message)
        failure.text = test_case.get("details", "No additional details provided")

    # Write the XML structure to a file
    tree = ET.ElementTree(testsuites)
    with open(output_file, "wb") as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)

    print(f"JUnit report generated: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python json_to_junit.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    
    # Read and parse the JSON file
    with open(json_file_path, 'r') as f:
        json_data = json.load(f)

    # Create the JUnit report
    create_junit_report(json_data)