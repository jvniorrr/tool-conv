import json, csv
import random, string
import sys, os, platform
import time
import import_functions, converterTools

#################################################
################  TO-DO  ########################
#   - Write IMPORT functions for PHANTOM, NOVA.
#   - Write EXPORT functions for DASHE, SPLASHFORCE. TBC...
#   - DONE: Import for CSV, and PRISM.
#   - DONE: Export to PRISM, PHANTOM, NOVA, SPLASHFORCE, DASHE. 
#   - Afer writing export functions, fix them to accept arguments. Accept a file, the list of profiles
#################################################
#################################################


# import_functions.from_csv()
# import_functions.from_csv("Sheet1.csv")

def randomString(stringLength=10):
    """Generate a random string of letters, digits and special characters """

    password_characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(password_characters) for i in range(stringLength))

# function to read in the json files each time
def read_from_json(file: str):
    """Accepts a json file and reads it"""
    if ".json" not in str(file):
        sys.exit("Please enter a json file from PrismAIO.")

    try:
        with open(file, "r") as file_object:
            parsed = json.load(file_object)
    except FileNotFoundError:
        sys.exit("Please supply a json file that exists.")
    except json.JSONDecodeError:
        sys.exit("File does not contain valid Json. Exiting program")
    
    return parsed

# write to file from here, also find out how to make a folder and write the profile file there
# maybe can make a function and write using that. 
def write_profile(bot: str, file_export: list):
    """Function accepts a path, and profiles which are to be exported/written to json file.
    This is the export function, which writes/makes new files.
    
    Parameters
    ----------
    - Bot: Accepts a path/the bot name to convert to proper name of export.
    - file_export: Profiles being exported to the new file, for certain bot. This can also be a dictionary value. 
    """

    systemType = platform.system().lower()
    file = f"{bot.lower()}.json"
    botFName = bot.title()
    currentDir = os.getcwd()
    exports = str(currentDir) + "/exports/"
    botFolder = str(exports) + f"{botFName}"
    if systemType.lower() == "windows":
        exports = str(currentDir) + '\exports'
        botFolder = str(exports) + f'\{botFName}'
        file_path = f'{botFolder}\{file}'
    else:
        file_path = f"{botFolder}/{file}"

    # check if the path already exists
    # make path to write file to/json export
    if not os.path.exists(exports):
        os.mkdir(exports)
        os.mkdir(botFolder)
    else:
        if not os.path.exists(botFolder):
            os.mkdir(botFolder)
        else:
            if os.path.exists(file_path):
                check = input("This File/Path already exists, would you like to:" + 
                "\n1: Replace File" + 
                "\n2: Rename Current File" +
                "\n3: Stop\n")
                if check == "2":
                    if systemType.lower() == "windows":
                        file_path = f'{botFolder}\copy of {file}'
                    else:
                        file_path = f"{botFolder}/copy of {file}"
                elif check == "3":
                    sys.exit("User Quit Program...")

    try:
        with open(file_path, "w") as file_object:
            json.dump(file_export, file_object)
            print(f"Completed converting your profile's. Check \n{file_path}")
    except Error as e:
        print(e)

def to_prism():
    """Currently accepts CSV file, and exports to PrismAIO json format. 
    """
    # use of the sheet
    profiles = import_functions.from_csv("Sheet1.csv")
    profiles_export = []
    i = 0

    # load in the profiles
    for profile in profiles:
        i += 1
        current = json.dumps(profile)
        current = json.loads(current)

        # convert number to prism format
        telephone_string = current["Billing Info"]["Telephone"].split()[0]
        area_code = telephone_string[:3]
        phone_pt_1 = telephone_string[3:6]
        phone_pt_2 = telephone_string[6:10]
        formatted_phone = f"({area_code}) {phone_pt_1}-{phone_pt_2}"

        # get random number to format the id for profile
        randomPt1 = randomString(8)
        randomPt2 = randomString(4)
        randomPt3 = randomString(4)
        randomPt4 = randomString(4)
        if int(i) >= 10:
            randomPt5 = randomString(11)
        else:
            randomPt5 = randomString(12)

        # get the timestamp for prism createdAt key value
        timestamp = int(str(time.time_ns())[:13])

        # convert card to prism format
        card = current["Payment Info"]["Card Number"]
        formatted_card = f"{card[:4]} {card[4:8]} {card[8:12]} {card[12:16]}"

        prism_profile = {
            "billing": {
                "address1": current["Billing Info"]["Billing Address Line 1"],
                "address2": current["Billing Info"]["Apt/Suite"],
                "city": current["Billing Info"]["Billing City"],
                # add error handling here on if it's entered as United States/US/USA, for country
                "country": "United States",
                "firstName": current["Billing Info"]["Billing Name"].split()[0],
                "lastName": current["Billing Info"]["Billing Name"].split()[1],
                "phone": formatted_phone,
                "postalCode": current["Billing Info"]["Billing Zipcode"],
                "province": current["Billing Info"]["Billing State"].title(), # state here, add error handling on if input is just CA
                "usesBillingInformation": current["Shipping Info"]["Same Ship/Bill"]
                },
            "createdAt": timestamp,
            "id": f"{randomPt1}-{randomPt2}-{randomPt3}-{randomPt4}-{randomPt5}{i}",
            "name": current["Profile Name"],
            "oneTimeUse": current["Payment Info"]["CheckoutLimit"],
            "payment": {
                "cvv": current["Payment Info"]["CVV"],
                "month": current["Payment Info"]["Exp Month"],
                "name": current["Payment Info"]["Card Name"],
                "num": formatted_card,
                "year": current["Payment Info"]["Exp Year"]
                },
            "shipping": {
                "address1": current["Shipping Info"]["Address Line 1"],
                "address2": current["Shipping Info"]["Apt/Suite"],
                "city": current["Shipping Info"]["Shipping City"],
                "country": current["Shipping Info"]["Shipping Country"],
                "email": current["Payment Info"]["Profile Email"],
                "firstName": current["Shipping Info"]["Shipping Name"].split()[0],
                "lastName": current["Shipping Info"]["Shipping Name"].split()[1],
                "phone": formatted_phone,
                "postalCode": current["Shipping Info"]["Zip Code"],
                "province": current["Shipping Info"]["Shipping State"].title() # add handling for states entered in different format 
                }
            }

        # add handling here later to change the shiiping address if it's false
        if current["Shipping Info"]["Same Ship/Bill"] == "false":
            prism_profile["billing"]["usesBillingInformation"] = False
        elif current["Shipping Info"]["Same Ship/Bill"] == "true":
            prism_profile["billing"]["usesBillingInformation"] = True
        
        # check if user wants more than 1 checkout per cc or not
        if current["Payment Info"]["CheckoutLimit"].lower() == "false":
            prism_profile["oneTimeUse"] = False
        elif current["Payment Info"]["CheckoutLimit"].lower() == "true":
            prism_profile["oneTimeUse"] = True
        
        # add to the list to add at the final
        profiles_export.append(prism_profile)
        print(f"Formatted {i} profile(s)")

    # export the file to the new folder
    write_profile("prism", profiles_export)
       
def to_phantom(file: str):
    """Currently accepts files from the CSV format and exports to a phantom json.
    File: Accepts the path to certain file. Accepts json from PrismAIO and also CSV sheet.
    """
    # use of the sheet
    profiles = file
    # print(profiles)

    # have all the profiles passed in stored in a list
    profiles_export = []
    i = 0

    # load in the profiles
    for profile in profiles:

        current = json.dumps(profile)
        current = json.loads(current)
        i += 1

        # convert the state here, with initials for Phantom. Have to add support for GB/EU still.
        convert_state = current["Billing Info"]["Billing State"].split()
        if len(convert_state) > 1:
            billing_state = convert_state[0][:1].upper() + convert_state[1][:1].upper()
        else:
            billing_state = convert_state[0][:2].upper()

        # check the cc type here
        cc_card = current["Payment Info"]["Card Number"]
        if cc_card[:1] == "3":
            cc_type = "amex"    
        elif cc_card[:1] == "4":
            cc_type = "visa"
        elif cc_card[:1] == "5":
            cc_type = "master"
        elif cc_card[:1] == "6":
            cc_type = "discover"

        # format to dict to export as json for phantom export
        profile_export = {
            "Billing": {
            "Address": current["Billing Info"]["Billing Address Line 1"],
            "Apt": current["Billing Info"]["Apt/Suite"],
            "City": current["Billing Info"]["Billing City"],
            "FirstName": current["Billing Info"]["Billing Name"].split()[0],
            "LastName": current["Billing Info"]["Billing Name"].split()[1],
            "State": billing_state,
            "Zip": current["Billing Info"]["Billing Zipcode"]
            },
            "CCNumber": current["Payment Info"]["Card Number"],
            "CVV": current["Payment Info"]["CVV"],
            "CardType": cc_type,
            "Country": "US", # add support here for other countries latter
            "Email": current["Payment Info"]["Profile Email"],
            "ExpMonth": current["Payment Info"]["Exp Month"],
            "ExpYear": current["Payment Info"]["Exp Year"],
            "Name": current["Profile Name"],
            "Phone": current["Billing Info"]["Telephone"],
            "Same": None,
            "Shipping": {
            "Address": current["Shipping Info"]["Address Line 1"],
            "Apt": current["Shipping Info"]["Apt/Suite"],
            "City": current["Shipping Info"]["Shipping City"],
            "FirstName": current["Shipping Info"]["Shipping Name"].split()[0],
            "LastName": current["Shipping Info"]["Shipping Name"].split()[1],
            "State": billing_state,
            "Zip": current["Shipping Info"]["Zip Code"]
            }
        }

        # set CC type outside till figure out how to explicity within json/dict
        # print(current["Payment Info"]["Card Number"])
        
        # set the same billing/ship if and not true.
        if not current["Shipping Info"]["Same Ship/Bill"]:
            profile_export["Same"] = False
        elif current["Shipping Info"]["Same Ship/Bill"]:
            profile_export["Same"] = True
        
        profiles_export.append(profile_export)
        print(f"Formatted {i} profile(s)")

    # make directory, where to write new files
    
    # write file now to a json file to a folder w/in the EXPORT folder, w/ phantom name 
    print(f"Converting: {i} profiles....")
    write_profile("Phantom", profiles_export)

def to_Nova():
    """
    Accepts in a list value and exports those profiles to NovaAIO 1.0 format. Doesn't work
    as intended, have to use aycd format for import to Nova.

    Parameters
    ----------
    file: list
        Pass in list from other import formats
    """
    # pass in an argument to read in the files, this case a list
    profiles_import = import_functions.from_csv("Sheet1.csv")

    # export dictionary
    exportDict = {
        "savedProfiles": None,
        "profileGroups": []
    }

    # list to store the values in exportDict
    savedProfilesValue = []
    i = 0

    # all profile's
    for profile in profiles_import:
        current = json.dumps(profile)
        current = json.loads(current)

        # convert country and countrycode for billing
        country_input = current["Billing Info"]["Billing Country"]
        countryAbbrev = converterTools.short2long(country_input, 's')
        countryLong = converterTools.short2long(country_input, 'l')

        if countryAbbrev.upper() == "US" or countryAbbrev.upper() == "CA":
            i += 1

            # convert the state to long version
            state = current["Billing Info"]["Billing State"]
            longState = converterTools.short2longState(state, "l", countryAbbrev.upper())
            shortState = converterTools.short2longState(state, "s", countryAbbrev.upper())

            # convert card type
            cardType = current["Payment Info"]["Card Type"].title()
            
            # format the cards to nova style
            expMonth = current["Payment Info"]["Exp Month"]
            expYear = current["Payment Info"]["Exp Year"][2:]
            expDate = f"{expMonth}/{expYear}"

            # format phone number
            phone = current["Shipping Info"]["Telephone"]
            areaCode = phone[:3]
            telPt1 = phone[3:6]
            telPt2 = phone[6:10]
            telephone = f"({areaCode}) {telPt1}-{telPt2}"

            # format profile in dictionary, then append this to list.
            exportProfile = {
                "billing": {
                    "address": current["Billing Info"]["Billing Address Line 1"],
                    "apt": current["Billing Info"]["Apt/Suite"],
                    "city": current["Billing Info"]["Billing City"],
                    "country": countryLong,
                    "countrycode": countryAbbrev,
                    "state": shortState,
                    "zip": current["Billing Info"]["Billing Zipcode"]
                },
                "cardholdername": current["Payment Info"]["Card Name"],
                "cardnumber": current["Payment Info"]["Card Number"],
                "cardtype": cardType,
                "cvv": current["Payment Info"]["CVV"],
                "email": current["Payment Info"]["Profile Email"],
                "expdate": expDate,
                "firstname": current["Payment Info"]["Card Name"].split()[0],
                "lastname": current["Payment Info"]["Card Name"].split()[1],
                "phone": telephone,
                "profilename": current["Profile Name"],
                "shipping": {
                    "address": current["Shipping Info"]["Address Line 1"],
                    "apt": current["Shipping Info"]["Apt/Suite"],
                    "city": current["Shipping Info"]["Shipping City"],
                    "country": countryLong,
                    "countrycode": countryAbbrev,
                    "state": shortState,
                    "zip": current["Shipping Info"]["Zip Code"]
                },
                "usebilling": current["Shipping Info"]["Same Ship/Bill"],
                "useonce": current["Payment Info"]["CheckoutLimit"]
            }

            # check if billing true or not.
            if exportProfile["usebilling"].lower() == "false":
                exportProfile["billing"]["address"] = ""
                exportProfile["billing"]["apt"] = ""
                exportProfile["billing"]["city"] = ""
                exportProfile["billing"]["country"] = countryLong
                exportProfile["billing"]["countrycode"] = countryAbbrev
                exportProfile["billing"]["state"] = shortState
                exportProfile["billing"]["zip"] = ""
                exportProfile["usebilling"] = False
            else:
                exportProfile["usebilling"] = True
            
            # check the checkout limit
            if current["Payment Info"]["CheckoutLimit"].lower() == "true":
                exportProfile["useonce"] = True
            else:
                exportProfile["useonce"] = False

            savedProfilesValue.append(exportProfile)
        else:
            print("Sorry currently do not support exporting to NovaAIO for EU profiles...")

    # write to dictionary as value
    exportDict["savedProfiles"] = savedProfilesValue
    # write profile to nova folder
    print(f"Converting: {i} profiles....")
    write_profile("Nova", exportDict)

def to_aycd():
    """
    Accepts in a list value and exports those profiles to NovaAIO 1.0 & AYCD format.

    Parameters
    ----------
    file: list
        Pass in list from other import formats
    """
    # pass in an argument to read in the files, this case a list
    profiles_import = import_functions.from_csv("PROFILES.csv")

    profiles = []

    # list to store the values in exportDict
    savedProfilesValue = []
    i = 0

    # all profile's
    for profile in profiles_import:
        current = json.dumps(profile)
        current = json.loads(current)

        # convert country and countrycode for billing
        country_input = current["Billing Info"]["Billing Country"]
        countryAbbrev = converterTools.short2long(country_input, 's')
        countryLong = converterTools.short2long(country_input, 'l')
        profileName = current["Profile Name"]

        if countryAbbrev.upper() == "US" or countryAbbrev.upper() == "CA":

            # convert the state to long version
            i += 1
            state = current["Billing Info"]["Billing State"]
            longState = converterTools.short2longState(state, "l", countryAbbrev.upper())
            shortState = converterTools.short2longState(state, "s", countryAbbrev.upper())
            
            # convert the ship state to long version
            shipState = current["Shipping Info"]["Shipping State"]
            shipLongState = converterTools.short2longState(shipState, "l", countryAbbrev.upper())

            dict = {
                "name": current["Profile Name"],
                "billingAddress": {
                    "name": current["Billing Info"]["Billing Name"],
                    "email": current["Payment Info"]["Profile Email"],
                    "phone": current["Billing Info"]["Telephone"],
                    "line1": current["Billing Info"]["Billing Address Line 1"],
                    "line2": current["Billing Info"]["Apt/Suite"],
                    "line3": "",
                    "postCode": current["Billing Info"]["Billing Zipcode"],
                    "city": current["Billing Info"]["Billing City"],
                    "state": longState,
                    "country": countryLong
                    },
                "shippingAddress": {
                    "name": current["Shipping Info"]["Shipping Name"],
                    "email": current["Payment Info"]["Profile Email"],
                    "phone": current["Shipping Info"]["Telephone"],
                    "line1": current["Shipping Info"]["Address Line 1"],
                    "line2": current["Shipping Info"]["Apt/Suite"],
                    "line3": "",
                    "postCode": current["Shipping Info"]["Zip Code"],
                    "city": current["Shipping Info"]["Shipping City"],
                    "state": shipLongState,
                    "country": countryLong
                    },
                "paymentDetails": {
                    "nameOnCard": current["Payment Info"]["Card Name"],
                    "cardType": current["Payment Info"]["Card Type"].title(),
                    "cardNumber": current["Payment Info"]["Card Number"],
                    "cardExpMonth": current["Payment Info"]["Exp Month"],
                    "cardExpYear": current["Payment Info"]["Exp Year"],
                    "cardCvv":  current["Payment Info"]["CVV"]
                    },
                "sameBillingAndShippingAddress": current["Shipping Info"]["Same Ship/Bill"].title(),
                "onlyCheckoutOnce": current["Payment Info"]["CheckoutLimit"].title(),
                "matchNameOnCardAndAddress": False
            }

            # add handling if user inputs 1 checkout or not
            if current["Shipping Info"]["Same Ship/Bill"].lower() == "true":
                dict["billingAddress"]["name"] = current["Shipping Info"]["Shipping Name"]
                dict["billingAddress"]["email"] = current["Payment Info"]["Profile Email"]
                dict["billingAddress"]["phone"] = current["Shipping Info"]["Telephone"]
                dict["billingAddress"]["line1"] = current["Shipping Info"]["Address Line 1"]
                dict["billingAddress"]["line2"] = current["Shipping Info"]["Apt/Suite"]
                dict["billingAddress"]["postCode"] = current["Shipping Info"]["Zip Code"]
                dict["billingAddress"]["city"] = current["Shipping Info"]["Shipping City"]
                dict["billingAddress"]["state"] = shipLongState
                dict["sameBillingAndShippingAddress"] = True
            else:
                dict["sameBillingAndShippingAddress"] = False

            # check if user wants one checkout or not
            if current["Payment Info"]["CheckoutLimit"].lower() == "true":
                dict["onlyCheckoutOnce"] = True
            else:
                dict["onlyCheckoutOnce"] = False

            savedProfilesValue.append(dict)

        else:
            print(f"Sorry currently don't support importing to Nova for EU profiles. Excluding Profile:  {profileName}")

    # write profile to nova folder
    print(f"Converting: {i} profiles....")
    write_profile("Nova", savedProfilesValue)
            
def to_splashforce():
    """
    Accepts in a list value and exports those profiles to SplashForce format.

    Parameters
    ----------
    file: list
        Pass in list from other import formats
    """
    profiles_import = import_functions.from_csv("Sheet1.csv")

    # list to store the values in exportDict
    savedProfilesValue = []
    i = 0

    # all profile's
    for profile in profiles_import:
        current = json.dumps(profile)
        current = json.loads(current)

        # store the country long
        bCountry = current["Billing Info"]["Billing Country"]
        billCountry = converterTools.short2long(bCountry, "l")
        billCountryAbbrev = converterTools.short2long(bCountry, "s")

        sCountry = current["Shipping Info"]["Shipping Country"]
        shipCountry = converterTools.short2long(sCountry, "l")
        shipCountryAbbrev = converterTools.short2long(sCountry, "s")

        i += 1

        dict = {
            "profileName": current["Profile Name"],
            "email": current["Payment Info"]["Profile Email"],
            "billingAddress": {
                "firstName": current["Billing Info"]["Billing Name"].split()[0],
                "lastName": current["Billing Info"]["Billing Name"].split()[1],
                "addressOne": current["Billing Info"]["Billing Address Line 1"],
                "addressTwo": current["Billing Info"]["Apt/Suite"],
                "zip": current["Billing Info"]["Billing Zipcode"],
                "city": current["Billing Info"]["Billing City"],
                "state": None,
                "country": billCountry,
                "phone": current["Billing Info"]["Telephone"]
                },
            "shippingAddress": {
                "firstName": current["Shipping Info"]["Shipping Name"].split()[0],
                "lastName": current["Shipping Info"]["Shipping Name"].split()[1],
                "addressOne": current["Shipping Info"]["Address Line 1"],
                "addressTwo": current["Shipping Info"]["Apt/Suite"],
                "zip": current["Shipping Info"]["Zip Code"],
                "city": current["Shipping Info"]["Shipping City"],
                "state": None,
                "country": shipCountry,
                "phone": current["Shipping Info"]["Telephone"]
                },
            "card": {
                "cardHolderName": current["Payment Info"]["Card Name"],
                "cardNumber": current["Payment Info"]["Card Number"],
                "cardExpiryMonth": current["Payment Info"]["Exp Month"],
                "cardExpiryYear": current["Payment Info"]["Exp Year"],
                "cardCVV": current["Payment Info"]["CVV"]
                },
            "jigAddress": False,
            "oneCheckout": False
        }

        if current["Payment Info"]["CheckoutLimit"].lower() == "true":
            dict["oneCheckout"] = True
        else:
            dict["oneCheckout"] = False

        if shipCountryAbbrev == "US" or shipCountryAbbrev == "CA":
            state = current["Shipping Info"]["Shipping State"]
            longState = converterTools.short2longState(state, "l", shipCountryAbbrev)
            dict["shippingAddress"]["state"] = longState
        if billCountryAbbrev == "US" or billCountryAbbrev == "CA":
            state = current["Billing Info"]["Billing State"]
            longState = converterTools.short2longState(state, "l", shipCountryAbbrev)
            dict["billingAddress"]["state"] = longState

        # add to the list to write
        savedProfilesValue.append(dict)

    # write the export to the json file
    print(f"Converting: {i} profiles....")
    write_profile("SplashForce", savedProfilesValue)

def to_dashe():
    """
    Accepts in a list value and exports those profiles to DasheV3 format.

    Parameters
    ----------
    file: list
        Pass in list from other import formats
    """
    profiles_import = import_functions.from_csv("Sheet1.csv")

    # list to store the values in exportDict
    savedProfilesValue = dict()
    i = 0

    # all profile's
    for profile in profiles_import:
        current = json.dumps(profile)
        current = json.loads(current)

        # store the country long
        bCountry = current["Billing Info"]["Billing Country"]
        billCountry = converterTools.short2long(bCountry, "l")
        billCountryAbbrev = converterTools.short2long(bCountry, "s")

        sCountry = current["Shipping Info"]["Shipping Country"]
        shipCountry = converterTools.short2long(sCountry, "l")
        shipCountryAbbrev = converterTools.short2long(sCountry, "s")
        profileName = current["Profile Name"]

        i += 1


        exportDict = {
        profileName: {
            "billing": {
                "address": current["Shipping Info"]["Address Line 1"],
                "apt": current["Shipping Info"]["Apt/Suite"],
                "city": current["Shipping Info"]["Shipping City"],
                "country": shipCountry,
                "firstName": current["Shipping Info"]["Shipping Name"].split()[0],
                "lastName": current["Shipping Info"]["Shipping Name"].split()[1],
                "phoneNumber": current["Shipping Info"]["Telephone"],
                "state": None,
                "zipCode": "90012"
                },
            "billingMatch": True,
            "card": {
                "cvv": current["Payment Info"]["CVV"],
                "holder": current["Payment Info"]["Card Name"],
                "month": current["Payment Info"]["Exp Month"],
                "number": current["Payment Info"]["Card Number"],
                "year": current["Payment Info"]["Exp Year"]
                },
            "email": current["Payment Info"]["Profile Email"],
            "profileName": current["Profile Name"],
            "shipping": {
                "address": current["Shipping Info"]["Address Line 1"],
                "apt": current["Shipping Info"]["Apt/Suite"],
                "city": current["Shipping Info"]["Shipping City"],
                "country": shipCountry,
                "firstName": current["Shipping Info"]["Shipping Name"].split()[0],
                "lastName": current["Shipping Info"]["Shipping Name"].split()[1],
                "phoneNumber": current["Shipping Info"]["Telephone"],
                "state": None,
                "zipCode": current["Shipping Info"]["Zip Code"]
                }
            }
        }

        if shipCountryAbbrev == "US" or shipCountryAbbrev == "CA":
            state = current["Shipping Info"]["Shipping State"]
            longState = converterTools.short2longState(state, "l", shipCountryAbbrev)
            exportDict[profileName]["shipping"]["state"] = longState
        if billCountryAbbrev == "US" or billCountryAbbrev == "CA":
            state = current["Billing Info"]["Billing State"]
            longState = converterTools.short2longState(state, "l", shipCountryAbbrev)
            exportDict[profileName]["billing"]["state"] = longState

        # check to see if user input true or false for same ship/bill
        if current["Shipping Info"]["Same Ship/Bill"].lower() == "false":
            exportDict[profileName]["billing"]["billingMatch"] = False
            exportDict[profileName]["billing"]["address"] = current["Billing Info"]["Billing Address Line 1"]
            exportDict[profileName]["billing"]["apt"] = current["Billing Info"]["Apt/Suite"]
            exportDict[profileName]["billing"]["city"] = current["Billing Info"]["Billing City"]
            exportDict[profileName]["billing"]["country"] = billCountry
            exportDict[profileName]["billing"]["firstName"] = current["Billing Info"]["Billing Name"].split()[0]
            exportDict[profileName]["billing"]["lastName"] = current["Billing Info"]["Billing Name"].split()[1]
            exportDict[profileName]["billing"]["phoneNumber"] = current["Billing Info"]["Telephone"]
            exportDict[profileName]["billing"]["zipCode"] = current["Billing Info"]["Billing Zipcode"]

        # print(exportDict)
        savedProfilesValue.update(exportDict)
    
    # write the export to the json file
    print(f"Converting: {i} profiles....")
    write_profile("Dashe", savedProfilesValue)

# to_dashe()
# prismImport = "/Users/junior/Desktop/Bots/profile-converter/exports/Prism/prism.json"
# from_prism(prismImport, "PhantoM")

# to_Nova()

# to_phantom()