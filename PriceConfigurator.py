import tkinter as tk
from tkinter import ttk
import csv
from tkinter import filedialog
from tkinter import messagebox
from tkinter import PhotoImage
from datetime import datetime, timedelta
import calendar
import PricingFunctions
from PricingFunctions import *
import os

# Create a dictionary to store the data
data = {}

# Create a dictionary to store the entry widgets
entries = {}

# Tracking Promo SKU
promo_skus = []
promo_sku = {}

# Global dictionary to keep track of the SKU to be deleted
delete_entries = {}

# File path for saving/loading data
data_file_path = "SF_Price_Configurator.csv"

# Filter values
filter_values = {}

# Filtered values
filtered_rows = []

# Assume your data is stored in a list of dictionaries for convenience
tab4_data = []
tab5_data = []
tab6_data = []
tab7_data = []

# Function to save data to CSV file
def save_data():
    with open(data_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data.keys())
        writer.writeheader()
        writer.writerows([dict(zip(data.keys(), values)) for values in zip(*data.values())])

# Validate File Input
#### NEEDS TO BE FIXED DUE TO ENCODING ISSUES ####
def csvValidator(csv_file_path):
    expected_columns = ["SKU", "ELEC", "GAS", "TERM", "GREEN", "OFF TYPE", 
                        "REV1", "REV2", "Green Type", "Term", "Commodity", 
                        "Electricity Rate", "Natural Gas Rate", "Admin Fee Elec", 
                        "Admin Fee Gas", "Type"]

    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        csv_columns = reader.fieldnames

    missing_columns = [column for column in expected_columns if column not in csv_columns]
    extra_columns = [column for column in csv_columns if column not in expected_columns]

    if missing_columns:
        print(f"Missing columns: {missing_columns}")
    if extra_columns:
        print(f"Extra columns: {extra_columns}")

    return not (missing_columns or extra_columns)

# Function to load data from CSV file
def load_data(csv_file_path):
    global data

    # Check if the CSV file is valid before loading the data
    if not csvValidator(csv_file_path):
        print("Invalid CSV file. Data was not loaded.")
        return

    data = {}
    with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile: # Notice the encoding parameter here
        reader = csv.DictReader(csvfile)
        for row in reader:
            for column, value in row.items():
                if column not in data:
                    data[column] = []
                data[column].append(value)

    # Refresh the data view after loading new data
    refresh_data_view()

# Function to select a CSV file and load data from it
def select_file():
    csv_file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if csv_file_path:
        load_data(csv_file_path)

# Function to add new SKU
def add_sku():
    add_sku_window = tk.Toplevel(root)
    add_sku_window.title("Add SKU")
    add_sku_window.attributes('-topmost', True)

    global promo_sku

    energy_type = tk.StringVar()  # Variable to hold selected radio button value
    promo_sku = tk.StringVar(value="N")  # Variable to hold promo SKU status
    # Create a separate StringVar for each radio button
    elec_type = tk.StringVar()
    gas_type = tk.StringVar()

    # Create a StringVar for energy type
    energy_dropdown = tk.StringVar()

    # Function to run when energy type is changed
    def energy_type_changed(*args):
        if energy_type.get() == "ELEC":
            elec_type.set(energy_dropdown.get())
            gas_type.set('X')
        elif energy_type.get() == "GAS":
            gas_type.set(energy_dropdown.get())
            elec_type.set('X')

    # Trace the energy type variable
    energy_type.trace('w', energy_type_changed)

    for i, column in enumerate(data.keys()):

        if column == "TERM":
            label = tk.Label(add_sku_window, text="Term Length")
            label.grid(row=i, column=0, pady=10)
            options = [1,2,3,5]
            entries[column] = tk.StringVar()
            dropdown = tk.OptionMenu(add_sku_window, entries[column], *options)
            dropdown.grid(row=i, column=1)

        elif column == "OFF TYPE":
            label = tk.Label(add_sku_window, text="Offer Type")
            label.grid(row=i, column=0, pady=10)
            options = ["R", "B"]
            entries[column] = tk.StringVar()
            dropdown = tk.OptionMenu(add_sku_window, entries[column], *options)
            dropdown.grid(row=i, column=1)

        elif column == "Green Type":
            label = tk.Label(add_sku_window, text="Green Type")
            label.grid(row=i, column=0, pady=10)
            options = ["standard", "green25", "green100"]
            entries[column] = tk.StringVar()
            dropdown = tk.OptionMenu(add_sku_window, entries[column], *options)
            dropdown.grid(row=i, column=1)

        elif column == "Commodity":
            label = tk.Label(add_sku_window, text="Commodity")
            label.grid(row=i, column=0, pady=10)
            options = ["Electric", "Gas"]
            entries[column] = tk.StringVar()
            dropdown = tk.OptionMenu(add_sku_window, entries[column], *options)
            dropdown.grid(row=i, column=1)

        elif column == "GREEN":
            label = tk.Label(add_sku_window, text="Add Green to SKU")
            label.grid(row=i, column=0, pady=10)
            entries[column] = tk.StringVar(value="X")
            green_button = tk.Checkbutton(add_sku_window, text="", variable=entries[column], onvalue="Y", offvalue="X")
            green_button.grid(row=i, column=1, pady=10)

        elif column in ["ELEC", "GAS"]:
            radio = tk.Radiobutton(add_sku_window, text=column, variable=energy_type, value=column)
            radio.grid(row=2, column=i-1, pady=10)
            entries[column] = elec_type if column == "ELEC" else gas_type
            label = tk.Label(add_sku_window, text="")
            label.grid(row=2, column=i+1, pady=10)
            dropdown = tk.OptionMenu(add_sku_window, energy_dropdown, "G", "V", "W")
            dropdown.grid(row=2, column=i+2)

        else:
            label = tk.Label(add_sku_window, text=column)
            label.grid(row=i, column=0, pady=10)
            entry = tk.Entry(add_sku_window)
            entry.grid(row=i, column=1, pady=10)
            entries[column] = entry


    # Promo SKU option
    label = tk.Label(add_sku_window, text="Promo SKU")
    label.grid(row=len(data.keys()), column=0, pady=10)
    promo_sku_button = tk.Checkbutton(add_sku_window, text="", variable=promo_sku, onvalue="Y", offvalue="N")
    promo_sku_button.grid(row=len(data.keys()), column=1, pady=10)

    submit_button = tk.Button(add_sku_window, text="Submit", command=submit)
    submit_button.grid(row=len(data.keys()) + 1, column=0, columnspan=2)



def delete_entry():
    # The SKU to delete is the text in the 'SKU' entry
    sku_to_delete = delete_entries['SKU'].get()

    # Remove the SKU from the lists in the data dictionary
    for key in data:
        if sku_to_delete in data[key] and sku_to_delete != "":
            data[key].remove(sku_to_delete)

            # If the SKU to delete exists in promo_skus list, remove it
            if sku_to_delete in promo_skus:
                promo_skus.remove(sku_to_delete)

                # If the SKU to delete exists in promo_sku dictionary, remove it
                if sku_to_delete in promo_sku:
                    del promo_sku[sku_to_delete]

            # Update your display or save data here if needed
            print(f'SKU {sku_to_delete} has been deleted from {key}.')
            refresh_data_view()
            break
    else:
        print(f'SKU {sku_to_delete} does not exist.')
        refresh_data_view()

# Function to delete SKU
def delete_sku():
    delete_sku_window = tk.Toplevel(root)
    delete_sku_window.title("Delete SKU")

    label = tk.Label(delete_sku_window, text='SKU')
    label.pack()
    entry = tk.Entry(delete_sku_window)
    entry.pack()
    delete_entries['SKU'] = entry

    delete_button = tk.Button(delete_sku_window, text="Delete", command=delete_entry)
    delete_button.pack()

# Function to create the filter window

############## CHECK IF SKU IS ALREADY IN DATA #####################
def create_filter_window():
    filter_window = tk.Toplevel(root)
    filter_window.title("Filter data")

    local_filter_entries = {}

    def local_apply_filter():
        for column, entry in local_filter_entries.items():
            entered_value = entry.get().strip()
            if entered_value:  # Only update if there's a value
                filter_values[column] = entered_value
            else:  # Remove the filter value if entry is empty
                filter_values.pop(column, None)
        refresh_data_view()

    for i, column in enumerate(data.keys()):
        label = tk.Label(filter_window, text=column)
        label.grid(row=i, column=0)
        entry_val = tk.StringVar(value=filter_values.get(column, ""))
        entry = tk.Entry(filter_window, textvariable=entry_val)
        entry.grid(row=i, column=1)
        local_filter_entries[column] = entry

    filter_button = tk.Button(filter_window, text="Filter", command=local_apply_filter)
    filter_button.grid(row=len(data.keys()) + 1, column=0, columnspan=2)

# Function to submit new data from the entry fields
def submit():
    global entries, promo_sku, promo_skus

    # Get the SKU from the entry widget
    entered_sku = entries['SKU'].get()

    # Check if the SKU already exists in the data
    if entered_sku in data['SKU']:
        # If it exists, display an error message and do not proceed
        messagebox.showerror("Error", f"SKU {entered_sku} already exists. Please enter a unique SKU.")
    elif entered_sku and entered_sku != '':
        # If it does not exist and is not empty, add it to the dictionary
        for column, entry in entries.items():
            data[column].append(entry.get())
        
        # If the Promo SKU option is selected, add the SKU to the promo_skus list
        if promo_sku.get() == 'Y':
            promo_skus.append(entered_sku)

        # Refresh the data view after submitting new data
        refresh_data_view()


# Function to apply filter
def apply_filter():
    # Updating the filter_values dict with current state of the entries
    for column, entry in filter_values.items():
        filter_values[column] = entry.get()
        
    # Now refresh the view
    refresh_data_view()

# Function to move filtered rows to Price Configurator tab
def move_filtered_rows():
    global filtered_rows
    filtered_rows = []

    for i, row in enumerate(zip(*data.values())):
        if all(filter_values.get(col, "").lower() in str(cell).lower() for col, cell in zip(data.keys(), row)) or all(not cell for cell in row):
            filtered_rows.append(row)
     
    # Clear existing widgets in tab3
    for widget in tab3.winfo_children():
        widget.destroy()

    # Extrapolate Data Button
    extrapolate_button = tk.Button(tab3, text="Extrapolate Data", command=extrapolate_data)
    extrapolate_button.pack()

    # Create a new treeview in tab3 for displaying the filtered rows
    filtered_tree = ttk.Treeview(tab3, show='headings')
    filtered_tree.pack(padx=50, pady=50, fill='both', expand=False)

    # Add columns to the filtered treeview
    filtered_tree["columns"] = list(data.keys())
    for column in filtered_tree["columns"]:
        filtered_tree.heading(column, text=column)

    # Insert the filtered rows into the filtered treeview
    for i, row in enumerate(filtered_rows):
        filtered_tree.insert("", "end", text=i, values=row)

    # Create a horizontal scrollbar
    x_scrollbar = ttk.Scrollbar(tab3, orient="horizontal", command=filtered_tree.xview)
    x_scrollbar.pack(side='bottom', fill='x')

    # Configure the treeview to use the scrollbar
    filtered_tree.configure(xscrollcommand=x_scrollbar.set)

    # Update the layout of the filtered treeview
    filtered_tree.pack()

    # Function to apply changes to all filtered rows
    def apply_changes():
        for row in filtered_rows:
            for column, entry in entries.items():
                row[data.keys().index(column)] = entry.get()

    # Add button to apply changes in tab3
    apply_button = tk.Button(tab3, text="Apply Changes", command=apply_changes)
    apply_button.grid(row=len(data.keys()) + 1, column=0, columnspan=2)

def edit_item(event):
    row_id = tree.selection()[0]
    column = tree.identify_column(event.x)
    col_num = int(column[1:]) - 1
    col_name = tree["columns"][col_num]
    cell_value = tree.item(row_id)['values'][col_num]

    # create edit window
    edit_root = tk.Toplevel(root)
    edit_root.title("Edit Item")

    # create label and entry
    edit_label = tk.Label(edit_root, text=f"Current Value: {cell_value}")
    edit_label.pack()
    new_val = tk.StringVar()
    edit_entry = tk.Entry(edit_root, textvariable=new_val)
    new_val.set(cell_value)
    edit_entry.pack()

    def update_item():
        # Check if SKU field is empty
        if col_name == "SKU" and not new_val.get().strip():
            messagebox.showerror("Invalid SKU", "SKU field cannot be empty.")
            return
        elif new_val.get() in data['SKU']:
            messagebox.showerror("Duplicate SKU", "The SKU value already exists in the table.")
            return

        # Update the TreeView
        tree.set(row_id, column, new_val.get())

        # Apply tag to the updated cell
        tag_name = f"edited_{row_id}_{col_num}"
        tree.tag_configure(tag_name, background="yellow")
        tree.item(row_id, tags=tag_name)
        
        # Also update the underlying data dictionary
        row_index = int(tree.item(row_id)['text'])
        data[col_name][row_index] = new_val.get()

        # Close the edit window
        edit_root.destroy()

    # create update button
    update_button = tk.Button(edit_root, text="Update Item", command=update_item)
    update_button.pack()

# Function to refresh the data view
def refresh_data_view():
    global promo_skus
    for child in tree.get_children():
        tree.delete(child)

    # Only add column headings if they don't exist
    if not tree["columns"]:
        tree["columns"] = list(data.keys())
        for column in tree["columns"]:
            tree.heading(column, text=column)
    
    for i, row in enumerate(zip(*data.values())):
        # Only show the row if it matches all non-empty filter values
        if all(filter_values.get(col, "").lower() in str(cell).lower() for col, cell in zip(data.keys(), row)) or all(not cell for cell in row):
            inserted_row = tree.insert('', 'end', text=i, values=row)
            # If the SKU is in promo_skus, apply the blue tag
            if row[0] in promo_skus:  # replace 0 with the appropriate index if SKU isn't the first column
                tag_name = f"promo_{i}"
                tree.tag_configure(tag_name, background="light green")
                tree.item(inserted_row, tags=tag_name)
     

# Function to download data CSV file
def download_file():
    download_directory = filedialog.askdirectory()
    if download_directory:
        destination = os.path.join(download_directory, os.path.basename(data_file_path))
        shutil.copy(data_file_path, destination)

# Saving data on button click
def on_button_click():
    save_data()

# Define each set of new columns for each tab
new_columns_tab4 = [
        "NAME", "CCRZ__SKU__C", "ENERGYDEFAULTPLAN__C", "ENERGYOFFERSUBTYPE__C", 
        "ENERGYOFFERTYPE__C", "ENERGY_CREDIT_CHECK_REQUIRED__C", "EVERGREENELIGIBLE__C", 
        "EVERGREENSKU__C", "EVERGREEN__C", "BUSINESSSTREAM__C", "CUSTOMERTYPE__C", 
        "ISBUNDLE__C", "ISELECTRICITY__C", "ISGAS__C", "PRICETYPEELECTRICITY__C", 
        "PRICETYPEGAS__C", "TERM__C", "CCRZ__STARTDATE__C", "CCRZ__ENDDATE__C", 
        "CCRZ__STOREFRONT__C", "SWITCH_RENEW_DEFAULT_PLAN__C", "CCRZ__PRODUCTSTATUS__C", 
        "ADMIN_FEE_DAILY_ELEC__C", "ADMIN_FEE_GAS_DAILY__C", "ADMIN_FEE_TYPE_ELEC__C", 
        "ADMIN_FEE_TYPE__C", "DISCOUNT_RATE_ELEC__C", "DISCOUNT_RATE_GAS__C", 
        "GREENTYPE__C", "GREEN_PREMIUM_PRICE__C", "AUTO_PRICE_COMPONENTS__C", 
        "ADMINFEEGAS__C", "ADMINFEESAVINGS__C", "ADMINFEE__C", "GASPRICE__C", 
        "GAS_PRICE_FEE__C", "GREEN_PRICE__C", "AdditionalSavings1__c", "AdditionalSavings2__c",
        "CustomTermsConditions__c"]

new_columns_tab5 = [
        "ccrz__SKU__c", "Commodity__c",	"Type__c", "Date_Range_Type__c", "Start_Month__c", "End_Month__c",
        "Start_Date__c", "End_Date__c",	"Rate__c", "Price_Floor__c", "Price_Ceiling__c", "Fee_Type__c",	"Admin_Discount__c",
        "Green_Energy_Percentage__c", "Green_Energy_Price__c", "Charge_Type__c", "Charge_Group_Code__c", 
        "Charge_Type_Description__c", "Marketable_Text__c", "Marketable_Text_Sequence__c"]

new_columns_tab6 = ["CCRZ__PRODUCT__C (SKU)",	"CCRZ__STARTDATE__C",	"CCRZ__ENDDATE__C",	"CCRZ__PRICE__C", "CCRZ__PRICELISTID__C"]

new_columns_tab7 = ["ccrz__Product__r.ccrz__SKU__c", "ccrz__SpecValue__c", "ccrz__Spec__r.ccrz__SpecID__c"]

# Define extrapolation methods for each tab
def extrapolate_for_tab4(filtered_rows):
    global tab4_data

    for rows in filtered_rows:
        # Determine the start and end dates
        now = datetime.now()  # Get the current date and time
        if now.month == 12:  # If the current month is December
            start_date = datetime(now.year + 1, 1, 1)  # Set the start date to the first day of the next year
        else:
            start_date = datetime(now.year, now.month + 1, 1)  # Set the start date to the first day of the next month

        name = "Energy Plan"
        sku = rows[0]

        energy_offer_type = PricingFunctions.energy_offer_type
        energyOfferType = energy_offer_type(rows[0])

        energy_offer_subtype = PricingFunctions.energy_offer_subtype
        energyOfferSubType = energy_offer_subtype(rows[0])

        is_bundle = PricingFunctions.is_bundle
        isBundle = is_bundle(rows[1], rows[2])

        is_electricity = PricingFunctions.is_electricity
        isElectricity = is_electricity(rows[10])

        is_gas = PricingFunctions.is_gas
        isGas = is_gas(rows[10])

        price_type_electricity = PricingFunctions.price_type_electricity
        priceTypeElectricity = price_type_electricity(rows[1])

        electricity_price = PricingFunctions.electricity_price
        electricityPrice = electricity_price(rows[11])

        gas_price = PricingFunctions.gas_price
        gasPrice = gas_price(rows[12])
        
        price_type_gas = PricingFunctions.price_type_gas
        priceTypeGas = price_type_gas(rows[2])

        green_type = PricingFunctions.green_type
        greenType = green_type(rows[8])

        term_c = PricingFunctions.term_c
        term = term_c(rows[3])

        product_status = PricingFunctions.product_status
        productStatus = product_status()

        admin_fee_elec_daily = PricingFunctions.admin_fee_elec_daily
        adminFeeElecDaily = admin_fee_elec_daily(rows[13])

        admin_fee_gas_daily = PricingFunctions.admin_fee_gas_daily
        adminFeeGasDaily = admin_fee_gas_daily(rows[14])

        start_date = start_date.strftime('%Y-%m-%d')
        end_date = ('2099-12-31')
        businessStream = "Energy" 

        # Check if SKU already exists in tab4_data
        existing_entry = next((item for item in tab4_data if item[1] == sku), None)
        if existing_entry:
            # If SKU exists, replace the old entry
            existing_entry_index = tab4_data.index(existing_entry)
            tab4_data[existing_entry_index] = (name, sku,"Energy Default Plan",energyOfferSubType, energyOfferType, "Energy Credit Check Required", "EVGE", "EVGSKU", "EVG", businessStream, "Cust Type", isBundle, isElectricity, isGas,
                                              priceTypeElectricity, priceTypeGas, term, start_date, end_date, "Store Front", "Switch", productStatus, adminFeeElecDaily, admin_fee_gas_daily, "AFTE", "AFT", "DRE", "DRG", greenType, "GPP",
                                              "APC", "AFG", "AFS", "AF", gasPrice, "GPF", "GreenP", "AS1", "AS2", "CTC")
        else:
            # If SKU does not exist, append the new row to tab6_data
            new_entry = (name, sku,"Energy Default Plan",energyOfferSubType, energyOfferType, "Energy Credit Check Required", "EVGE", "EVGSKU", "EVG", businessStream, "Cust Type", isBundle, isElectricity, isGas,
                        priceTypeElectricity, priceTypeGas, term, start_date, end_date, "Store Front", "Switch", productStatus, adminFeeElecDaily, admin_fee_gas_daily, "AFTE", "AFT", "DRE", "DRG", greenType, "GPP",
                        "APC", "AFG", "AFS", "AF", gasPrice, "GPF", "GreenP", "AS1", "AS2", "CTC")
            tab4_data.append(new_entry)

    return tab4_data

def extrapolate_for_tab5(filtered_rows):
    global tab5_data  

    for rows in filtered_rows:
        # Determine the start and end dates
        now = datetime.now()  # Get the current date and time
        if now.month == 12:  # If the current month is December
            start_date = datetime(now.year + 1, 1, 1)  # Set the start date to the first day of the next year
        else:
            start_date = datetime(now.year, now.month + 1, 1)  # Set the start date to the first day of the next month

        def check_rate(rate):
            if rate.isnumeric():
                return rate
            else:
                return None
        
        sku = rows[0]
        commod = rows[10]
        type_c = ""
        date_range_type = ""
        start_month = ""
        end_month = ""
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = ('2099-12-31')
        rate = rows[11][1:7] + rows[12][1:7]
        rate = check_rate(rate)
        price_floor = ""
        price_ceil = ""
        fee_type = ""
        admin_discount = ""
        green_energy_percent = ""
        green_energy_price = ""
        charge_type = ""
        charge_group = ""
        charge_type_des = ""
        market_text = ""
        market_text_seq = ""

        # Check if SKU already exists in tab5_data
        existing_entry = next((item for item in tab5_data if item[0] == sku), None)
        if existing_entry:
            # If SKU exists, replace the old entry
            existing_entry_index = tab5_data.index(existing_entry)
            tab5_data[existing_entry_index] = (sku, commod, type_c, date_range_type, start_month, end_month, start_date, end_date, rate, price_floor, price_ceil, fee_type, admin_discount, green_energy_percent, green_energy_price, charge_type, charge_group,
                                              charge_type_des, market_text, market_text_seq)
        else:
            # If SKU does not exist, append the new row to tab5_data
            new_entry = (sku, commod, type_c, date_range_type, start_month, end_month, start_date, end_date, rate, price_floor, price_ceil, fee_type, admin_discount, green_energy_percent, green_energy_price, charge_type, charge_group,
                        charge_type_des, market_text, market_text_seq)
            tab5_data.append(new_entry)

    return tab5_data

def extrapolate_for_tab6(filtered_rows):
    global tab6_data 

    for row in filtered_rows:
        sku = row[0]  # Assuming SKU maps to CCRZ__PRODUCT__C (SKU)

        # Determine the start and end dates
        now = datetime.now()  # Get the current date and time
        if now.month == 12:  # If the current month is December
            start_date = datetime(now.year + 1, 1, 1)  # Set the start date to the first day of the next year
        else:
            start_date = datetime(now.year, now.month + 1, 1)  # Set the start date to the first day of the next month

        #term_years = int(row[3])  # Assuming "term" column is at index 3 and represents number of years
        #end_date = datetime(start_date.year + term_years, start_date.month, 1) - timedelta(days=1)  # Subtract 1 day from the first day of the month after the term ends to get the last day of the term
        
        # Convert dates to strings in the format 'YYYY-MM-DD'
        start_date = start_date.strftime('%Y-%m-%d')
        #end_date = end_date.strftime('2099-12-31')
        end_date = ('2099-12-31')

        price = row[11] + row[12]

        # Check if SKU already exists in tab6_data
        existing_entry = next((item for item in tab6_data if item[0] == sku), None)
        if existing_entry:
            # If SKU exists, replace the old entry
            existing_entry_index = tab6_data.index(existing_entry)
            tab6_data[existing_entry_index] = (sku, start_date, end_date, price)
        else:
            # If SKU does not exist, append the new row to tab6_data
            new_entry = (sku, start_date, end_date, price)
            tab6_data.append(new_entry)

    # Save the updated data to a file every time the function is called
    with open('tab6_data.txt', 'w') as file:
        file.write(str(tab6_data))

    return tab6_data

def extrapolate_for_tab7(filtered_rows):
    global tab7_data  

    for row in filtered_rows:
        sku = row[0]
        # Check if SKU already exists in tab7_data
        if sku in tab7_data:
            # If SKU exists, it's already in the list. No action needed.
            pass
        else:
            # If SKU does not exist, append the new row to tab7_data
            tab7_data.append(sku)

    return tab7_data

# Function for extrapolating data to mapped states
def extrapolate_data():
    global filtered_rows
    filtered_data = filtered_rows

    # Extrapolate data for each tab and create corresponding TreeViews
    for tab, new_columns, extrapolation_method in [
        (tab4, new_columns_tab4, extrapolate_for_tab4),
        (tab5, new_columns_tab5, extrapolate_for_tab5),
        (tab6, new_columns_tab6, extrapolate_for_tab6),
        (tab7, new_columns_tab7, extrapolate_for_tab7)
    ]:
        # Clear existing widgets in the tab
        for widget in tab.winfo_children():
            widget.destroy()

        # Apply extrapolation transformations 
        extrapolated_data = extrapolation_method(filtered_rows)

        # Create a new TreeView for displaying the extrapolated data
        extrapolated_tree = ttk.Treeview(tab, show='headings')
        extrapolated_tree.pack(padx=50, pady=50, fill='both', expand=False)

        # Add columns to the TreeView
        extrapolated_tree["columns"] = new_columns
        for column in extrapolated_tree["columns"]:
            extrapolated_tree.heading(column, text=column)

        # Insert the extrapolated data into the TreeView
        for i, row in enumerate(extrapolated_data):
            extrapolated_tree.insert("", "end", text=i, values=row)

        # Create a horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(tab, orient="horizontal", command=extrapolated_tree.xview)
        x_scrollbar.pack(side='bottom', fill='x')
        extrapolated_tree.configure(xscrollcommand=x_scrollbar.set)

root = tk.Tk()
root.title("Price Configurator v.1")
root.geometry('1080x720')
root.state("zoomed")

style = ttk.Style(root)
style.theme_use("classic")

# ATCOEnergy Logo
image = PhotoImage(file="AtcoEnergyLogoTM - 175x54.png")
image_label = tk.Label(root, image=image)
image_label.pack(anchor = 'nw', padx = 10, pady = 10)

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=False)

######################################### Tab 1 #########################################
# Tab 1
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Data Entry") 

select_file_button = tk.Button(tab1, text="Select CSV File", command=select_file)
select_file_button.grid(row=0, column=0, columnspan=2)

######################################### Tab 2 #########################################
# Tab 2
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Data Preview")

# Frame for buttons
button_frame = tk.Frame(tab2)
button_frame.pack()

# Filter Button
filter_button = tk.Button(button_frame, text="Filter", command=create_filter_window)
filter_button.pack(side='left')

# Move Filter Items Button
move_filter_button = tk.Button(button_frame, text="Edit Filtered Items", command=move_filtered_rows)
move_filter_button.pack(side='left')

tree = ttk.Treeview(tab2, show='headings')
tree.pack(padx=50, pady=50, fill='both', expand=False)
tree.bind('<Double-1>', edit_item)

# Add download button in the Data View page
download_button = tk.Button(button_frame, text="Download CSV", command=download_file)
download_button.pack(side='left')

# Save button
button = tk.Button(tab2, text="Save", command=on_button_click)
button.pack()

# Add SKU
add_sku_button = tk.Button(button_frame, text="Add SKU", command=add_sku)
add_sku_button.pack(side='left')

# Delete SKU
delete_sku_button = tk.Button(button_frame, text="Delete SKU", command=delete_sku)
delete_sku_button.pack(side='left')

# Horizontal Scrolling
xsb = ttk.Scrollbar(tab2, orient="horizontal", command=tree.xview)
xsb.pack(fill='x')
tree.configure(xscrollcommand=xsb.set)

######################################### Tab 3 #########################################

# Tab 3 
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Price Configurator")

######################################### Tab 4 #########################################

# Tab 4
tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="CC Product Templates", )

######################################### Tab 5 #########################################

# Tab 5
tab5 = ttk.Frame(notebook)
notebook.add(tab5, text="Price Component")

######################################### Tab 6 #########################################

# Tab 6
tab6 = ttk.Frame(notebook)
notebook.add(tab6, text="Price List")

######################################### Tab 7 #########################################

# Tab 7
tab7 = ttk.Frame(notebook)
notebook.add(tab7, text="Product Specifications")

# Load data if file exists
if os.path.exists(data_file_path):
    load_data(data_file_path)

root.mainloop()


