import os
import sys
import logging
import pandas as pd
from xml.etree import ElementTree as ET
from tkinter import Tk, filedialog, messagebox

# Setup logging
logging.basicConfig(filename='ecu_parser.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_fields(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        containers = []
        sub_containers = []

        for container in root.findall('.//CONTAINERS/ECUC-CONTAINER-VALUE'):
            containers.append({
                'Container SHORT-NAME': container.find('.//SHORT-NAME').text,
                'Container DEFINITION-REFERENCE': container.find('.//DEFINITION-REF').text
            })

        for sub_container in root.findall('.//SUB-CONTAINERS/ECUC-CONTAINER-VALUE'):
            sub_containers.append({
                'Sub-Container SHORT-NAME': sub_container.find('.//SHORT-NAME').text,
                'Sub-Container DEFINITION-REFERENCE': sub_container.find('.//DEFINITION-REF').text
            })

        return containers, sub_containers
    except Exception as e:
        logging.error(f"Error occurred while extracting fields: {str(e)}")
        raise

def save_to_excel(containers, sub_containers, output_file):
    try:
        df_containers = pd.DataFrame(containers)
        df_sub_containers = pd.DataFrame(sub_containers)

        with pd.ExcelWriter(output_file) as writer:
            df_containers.to_excel(writer, sheet_name='Containers', index=False)
            df_sub_containers.to_excel(writer, sheet_name='Sub-Containers', index=False)
    except Exception as e:
        logging.error(f"Error occurred while saving to Excel: {str(e)}")
        raise

def main_gui():
    try:
        root = Tk()
        root.withdraw()
        xml_file_path = filedialog.askopenfilename(title="Select ECU XML file", filetypes=[("XML files", "*.xml")])

        if not xml_file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        output_file_path = filedialog.asksaveasfilename(title="Save as", defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

        if not output_file_path:
            messagebox.showerror("Error", "No output file selected.")
            return

        containers, sub_containers = extract_fields(xml_file_path)
        save_to_excel(containers, sub_containers, output_file_path)

        messagebox.showinfo("Success", "Extraction completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        logging.error(f"Error occurred: {str(e)}")

def main_cmd(xml_file_path, output_file_path):
    try:
        containers, sub_containers = extract_fields(xml_file_path)
        save_to_excel(containers, sub_containers, output_file_path)
        print("Extraction completed successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cmd":
        if len(sys.argv) != 4:
            print("Usage: python script.py cmd <xml_file_path> <output_file_path>")
            sys.exit(1)
        xml_file_path = sys.argv[2]
        output_file_path = sys.argv[3]
        main_cmd(xml_file_path, output_file_path)
    else:
        main_gui()
