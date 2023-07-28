############# CC Product Template #############
def energy_offer_type(sku):
    if sku[4] == "R" or sku[4] == "E":
        eot = "Home"
    elif sku[4] == "B" or sku[4] == "1" or sku[4] == "2":
        eot = "Business"
    return eot

def energy_offer_subtype(sku):
    if sku[4] == "R" or sku[4] == "B":
        eost = "Regular"
    elif sku[4] == "E":
        eost = "Employee"
    elif sku[4] == 1:
        eost = "Preferred"
    elif sku[4] == 2:
        eost = "Elite"
    return eost

def is_bundle(elec, gas):
    if elec == "X" and gas == "X":
        return True
    else:
        return False

def is_electricity(commodity):
    if commodity == "Electricity":
        ise = "TRUE"
    else:
        ise = "FALSE"
    return ise

def is_gas(commodity):
    if commodity == "Gas":
        isg = "TRUE"
    else:
        isg = "FALSE"
    return isg

def price_type_electricity(electype):
    if electype == "X":
        pte = "None"
    elif electype == "G":
        pte = "Guaranteed"
    elif electype == "V":
        pte = "Variable"
    elif electype == "W":
        pte = "Wholesale"
    return pte

def electricity_price(elecRate):
    ep = elecRate
    return ep

def price_type_gas(gastype):
    if gastype == "X":
        ptg = "None"
    elif gastype == "G":
        ptg = "Guaranteed"
    elif gastype == "V":
        ptg = "Variable"
    elif gastype == "W":
        ptg = "Wholesale"
    return ptg

def gas_price(natGasRate):
    gp = natGasRate
    return gp

def green_type(greentype):
    gt = greentype
    return gt

def term_c(termlen):
    tl = termlen
    return tl

def energy_default_plan():
    return

def switch_renew_default_plan():
    return

def evergreen_eligible():
    return

def evergreen_sku():
    return

def evergreen():
    evg = "FALSE"
    return evg

def energy_credit_check_required():
    return

def additional_savings1():
    return

def additional_savings2():
    return

def custom_terms_conditions():
    return

def campaign_id():
    return

def product_status():
    ps = "In Creation"
    return 

def admin_fee_elec_daily(fee):
    afed = fee
    return afed

def admin_fee_gas_daily(fee):
    afgd = fee
    return afgd

def admin_feetype_elec():
    return

def admin_fee_type():
    return

def discount_rate_elec():
    return

def discount_rate_gas():
    return

def green_premium():
    return

def auto_price_comps():
    return

def admin_fee_gas():
    return

def admin_fee_savings():
    return

def green_price():
    return





############# Price Component #############