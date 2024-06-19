import pandas as pd
import xml.etree.ElementTree as ET
import argparse

# Function to parse metadata and create CSV
def create_csv(metadata_file, controlling_field, controlled_field):
    print(f"Parsing metadata file: {metadata_file}")
    tree = ET.parse(metadata_file)
    root = tree.getroot()
    print(ET.tostring(root, encoding='utf8').decode('utf8'))

    print("Searching for CustomField elements...")
    dependencies = []
    namespace = "{http://soap.sforce.com/2006/04/metadata}"        

    for value_set in root.findall(f".//{namespace}valueSettings"):
        value_name_elem = value_set.find(f"{namespace}valueName")
        controlling_values_elem = value_set.findall(f"{namespace}controllingFieldValue")
        for control_value in controlling_values_elem:
            if value_name_elem is None:
                print(f"Warning: valueName not found in {ET.tostring(value_set, encoding='utf8').decode('utf8')}")
            if control_value is None:
                print(f"Warning: controllingFieldValues not found in {ET.tostring(value_set, encoding='utf8').decode('utf8')}")
            if value_name_elem is not None and control_value is not None:
                value_name = value_name_elem.text
                control_value = control_value.text
                dependencies.append([control_value, value_name])
                print(f"Dependency found - Controlling Value: {control_value}, Dependent Value: {value_name}")

    
    # Create DataFrame and CSV
    df = pd.DataFrame(dependencies, columns=[controlling_field, controlled_field])
    if not df.empty:
        output_file = 'picklist_dependency_matrix.csv'
        df.to_csv(output_file, index=False)
        print(f"CSV file created: {output_file}")
    else:
        print("No dependencies found.")

# Argument parser for command line arguments
def main():
    parser = argparse.ArgumentParser(description='Generate CSV for Salesforce picklist dependencies.')
    parser.add_argument('metadata_file', type=str, help='Path to the Department__c metadata file')
    parser.add_argument('controlling_field', type=str, help='API name of the controlling field')
    parser.add_argument('controlled_field', type=str, help='API name of the controlled field')
    
    args = parser.parse_args()
    
    create_csv(args.metadata_file, args.controlling_field, args.controlled_field)

if __name__ == "__main__":
    main()
