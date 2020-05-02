import os, csv, sys
import converterTools


def from_csv(file: str):
    """
    Prepares Profiles for 3rd party software from csv format.
    So far only accepts CSV, and exports to Phantom or Prism*.
    Download the file as a CSV format and pass the path to this function....

    Parameters
    ----------
    file: str
        Should be a '.csv' file path, just pass the path as a string as arg
    """
    # check the file that is passed, make sure it is a valid path
    if not os.path.exists(file):
        sys.exit("Please enter a valid csv path...")
    # prepares profiles for 3rd party software from csv format
    
    # return profile_dict
    profiles = []

    with open(file) as csv_file:
            fileReader = csv.reader(csv_file)

            # skip the first row
            next(fileReader)
            i = 1
            for row in fileReader:

                Profile_Name = row[1]
                profile_email = row[0]

                # credit card info
                checkout_limits = row[2]
                profile_card_name = row[3]
                profile_card_type = row[4]
                profile_card_number = row[5]

                profile_exp_month = row[6]

                # check to see if profile's have 1 or 2 digits for Exp Month
                if (len(profile_exp_month) == 1) and (int(profile_exp_month) <= 9):
                    profile_exp_month = "0" + profile_exp_month
                
                # add handling if user inputs info such as year '22 not 2022
                profile_exp_year = row[7]
                if len(profile_exp_year) == 2:
                    profile_exp_year = "20" + profile_exp_year
                    if (int(profile_exp_year) < 2020) or (int(profile_exp_year) > 2045):
                        expYearInput_msg = f"Profile: '{Profile_Name}' has an Expiration Year of {profile_exp_year}\n" 
                        expYearInput_msg +=  f"Are you sure this is correct? (Y/N)\n"
                        expYearInput = input(expYearInput_msg)
                        if expYearInput.lower() == "n":
                            sys.exit("Exiting program... Please fix your profiles.")
                        elif expYearInput.lower() == "y":
                            print("Ok. Continuing..")
                        # ask user if they would like to fix
                # if len(profile_exp_year) != 4:
                #     print(f"{Profile_Name}: Make sure to input 2 digits for the Exp Month & 4 Digits for the Exp Year"
                profile_cvv = row[8]
                
                # format cc here=
                if " " in profile_card_number:
                    cc_num = profile_card_number.replace(' ', '')
                else:
                    cc_num = profile_card_number
                if len(cc_num) < 15:
                    exit_msg = f"Profile: {Profile_Name} CC doesn't seem to have suffiecient numbers. Check the info."
                    sys.exit(exit_msg)

                # profile ship address/info
                profile_ship_name = row[10]
                if (not row[11].isdigit()) and (len(str(row[11]) != 10)):
                    print(f"Fix profile {i}, seems to be an issue with your number")
                    break
                else:
                    profile_phone = row[11]
                    
                profile_address = row[12]
                profile_address_2 = row[13]
                profile_address_3 = row[14]
                profile_zip = row[15]
                profile_city = row[16]
                profile_state = row[17]
                profile_country = row[18]
                profile_bill_ship = row[9]

                abbrevCountry_ship = converterTools.short2long(profile_country, "s")
                # check the state category here to make sure its valid for user, confirming they are in either US or CA
                # if abbrevCountry_ship == "US" or "CA":
                #     if not len(profile_state) > 1:
                #         state_msg = f"Please enter a valid state for your Profile: {Profile_Name}."
                #         sys.exit(state_msg)
                #     else:
                        # just have the State stored in case, use later possibly.
                if abbrevCountry_ship == "US":
                    if len(profile_state) < 1:
                        state_msg = f"Please enter a valid state for your Profile: {Profile_Name}."
                        sys.exit(state_msg)
                    else:
                        abbrevState = converterTools.short2longState(profile_state, "s", "US")
                elif abbrevCountry_ship == "CA":
                    if len(profile_state) < 1:
                        state_msg = f"Please enter a valid state for your Profile: {Profile_Name}."
                        sys.exit(state_msg)
                    else:
                        abbrevState = converterTools.short2longState(profile_state, "s", "CA")
                else:
                    abbrevState = None

                # profile billing address
                billing_name = row[19]
                billing_phone = row[20]
                billing_address = row[21]
                billing_address_2 = row[22]
                billing_address_3 = row[23]
                billing_zip = row[24]
                billing_city = row[25]
                billing_state = row[26]
                billing_country = row[27]
                
                abbrevCountry = converterTools.short2long(billing_country, "s")
            
                # set profile dictionary
                profile_dict = dict()
                profile_dict = {
                    "Profile Name": Profile_Name,

                    "Payment Info": {
                        "Profile Email": profile_email,
                        "Card Name": profile_card_name,
                        "Card Type": profile_card_type,
                        "Card Number": cc_num,
                        "Exp Month": profile_exp_month,
                        "Exp Year": profile_exp_year,
                        "CVV": profile_cvv,
                        "CheckoutLimit": checkout_limits
                    },

                    "Shipping Info": {
                        "Same Ship/Bill": profile_bill_ship,
                        "Shipping Name": profile_ship_name,
                        "Telephone": profile_phone,
                        "Address Line 1": profile_address,
                        "Apt/Suite": profile_address_2,
                        "Zip Code": profile_zip,
                        "Shipping City": profile_city,
                        "Shipping State": profile_state,
                        "Shipping Country": profile_country
                    },
                    "Billing Info": {
                        "Billing Name": billing_name,
                        "Telephone":profile_phone,
                        "Billing Address Line 1": profile_address,
                        "Apt/Suite": profile_address_2,
                        "Billing Zipcode": profile_zip,
                        "Billing City": profile_city,
                        "Billing State": profile_state,
                        "Billing Country": profile_country
                    }
                }
                if len(billing_address_3) > 1:
                    profile_dict["Address Line 3"] = profile_address_3

                if profile_bill_ship.lower() == "false":
                    profile_dict["Billing Info"] = dict()
                    profile_dict["Billing Info"]["Billing Name"] = billing_name
                    profile_dict["Billing Info"]["Telephone"] = billing_phone
                    profile_dict["Billing Info"]["Billing Address Line 1"] = billing_address
                    profile_dict["Billing Info"]["Apt/Suite"] = billing_address_2
                    profile_dict["Billing Info"]["Billing Zipcode"] = billing_zip
                    profile_dict["Billing Info"]["Billing City"] = billing_city
                    profile_dict["Billing Info"]["Billing State"] = billing_state
                    profile_dict["Billing Info"]["Billing Country"] = billing_country

                if not abbrevCountry.upper() == "US":
                    if not abbrevCountry.upper() == "CA":
                        profile_dict["Billing Info"]["Billing State"] = None
                if abbrevCountry_ship.upper() != "US":
                    if abbrevCountry_ship.upper() != "CA":
                        profile_dict["Shipping Info"]["Shipping State"] = None

                profiles.append(profile_dict)
                i += 1
                # print(profile_dict)
    return profiles

def from_prism(file: str, expBot: str):
    """Accepts json file from PrismAIO and converts for use to export profiles for other bots
    file: A path from where the json is located. Make sure its a .json
    expBot: Bot to export to; input is a string, currently support just 'phantom'."""
    # store all the profiles in a list
    profiles_formatted = []

    # read in the json file
    profiles_imported = read_from_json(file)
    # print(profiles_imported)

    # parse through each profile and format it properly
    for profile in profiles_imported:

        # format name
        shipName = profile["shipping"]["firstName"].title() + " " + profile["shipping"]["lastName"].title()
        billName = profile["billing"]["firstName"].title() + " " + profile["billing"]["lastName"].title()

        # format numbers from prism since it has space each 4 char and set into dictionary
        cc_number_list = str(profile["payment"]["num"])
        cc_number = cc_number_list[:4] + cc_number_list[5:9] + cc_number_list[10:14] + cc_number_list[15:]

        # format telephone from prism
        telephone = profile["billing"]["phone"].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')

        profile_export = {
            "Profile Name": profile["name"],
            "Payment Info": {
                "Profile Email": profile["shipping"]["email"],
                "Card Name": profile["payment"]["name"],
                # "Card Type": profile_card_type, # set this later, to accept and handle the card type in an outside loop
                "Card Number": cc_number,
                "Exp Month": profile["payment"]["month"],
                "Exp Year": profile["payment"]["year"],
                "CVV": profile["payment"]["cvv"],
                "CheckoutLimit": profile["oneTimeUse"]
            },
            "Shipping Info": {
                "Same Ship/Bill": profile["billing"]["usesBillingInformation"],
                "Shipping Name": shipName,
                "Telephone": telephone,
                "Address Line 1": profile["shipping"]["address1"],
                "Apt/Suite": profile["shipping"]["address2"],
                "Zip Code": profile["shipping"]["postalCode"],
                "Shipping City": profile["shipping"]["city"],
                "Shipping State": profile["shipping"]["province"],
                "Shipping Country": profile["shipping"]["country"]
            },
            "Billing Info": {
                "Billing Name": billName,
                "Telephone":telephone,
                "Billing Address Line 1": profile["billing"]["address1"],
                "Apt/Suite": profile["billing"]["address2"],
                "Billing Zipcode": profile["billing"]["postalCode"],
                "Billing City": profile["billing"]["city"],
                "Billing State": profile["billing"]["province"],
                "Billing Country": profile["billing"]["country"]
            }
        }

        # export profiles to list
        profiles_formatted.append(profile_export)

    # check the other arg, see what export user would like
    if expBot.lower() == "phantom":
        to_phantom(profiles_formatted)
        

