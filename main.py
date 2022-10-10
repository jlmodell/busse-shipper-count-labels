from blabel import LabelWriter
import os

def check_for_c_temp():
    if not os.path.exists(r"c:\temp"):
        os.mkdir(r"c:\temp")
    
    return os.path.join(r"c:\temp")

def check_for_sales_order_data():
    file_path = r"c:\temp"
    file_name = "sales_order_data.csv"
    file = os.path.join(file_path, file_name)

    if not os.path.exists(file):
        print("File not found: {}".format(file))
        exit(1)
    
    return file

def resource_path(relative_path):
    return os.path.join(r"c:\temp", "busse-shipper-count-labels", relative_path)

def generate_labels_pdf():

    try:
        check_for_c_temp()
        file = check_for_sales_order_data()
    except:
        print("Error creating c:\temp folder")
        exit(1)

    with open(file, "r") as f:
        data = f.readlines()
        # sales_order_number, number_of_labels
        data = [x.strip().split(",") for x in data]
    
    for order in data:
        sales_order_number = order[0]
        number_of_labels = int(order[1])

        print("Generating labels for Sales Order Number: {}".format(sales_order_number))
        print("Number of labels: {}".format(number_of_labels))

        target = rf'c:\temp\{sales_order_number}.pdf'

        records = [
            dict(
                so=f"{sales_order_number}", 
                count=x+1, 
                total=number_of_labels) 
            for x in range(number_of_labels)
        ]

        try:
            label_writer = LabelWriter(resource_path("template.html"), default_stylesheets=(resource_path("style.css"),))
            label_writer.write_labels(records, target=target)
        except:
            print("Error generating labels")
            exit(1)
        
        os.system(target)
    
    print("Done.")

    

if __name__ == "__main__":
    generate_labels_pdf()