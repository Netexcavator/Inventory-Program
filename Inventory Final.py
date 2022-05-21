import gspread


gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('15bYAOhMFSuFqMTEBWFBF1b7gOZLhxTeWIOnTtFlC9zM')
worksheet = sh.sheet1

#Sheet holds Inventory
worksheet = sh.sheet1

#Starting inventory of store by checking sheet
items = (worksheet.col_values(1)[1:])
prices = (worksheet.col_values(2)[1:])
stock = (worksheet.col_values(3)[1:])
inventory = {items:prices for items, prices in zip(items, prices)}
supply = {items:stock for items, stock in zip(items, stock)}
cart = {}

#Update dictionary whenevver a change is made in worksheet
def update_dictionaries():
    global items, prices, stock, inventory, supply
    items = (worksheet.col_values(1)[1:])
    prices = (worksheet.col_values(2)[1:])
    stock = (worksheet.col_values(3)[1:])
    inventory = {items:prices for items, prices in zip(items, prices)}
    supply = {items:stock for items, stock in zip(items, stock)}

def spacing():
    print('\n')

def home_screen():
    global direction
    print('Welcome to Pelle Produce', 'What would you like?', 'See Items', 'Admin Login', sep='\n')
    direction = input('Choose one :')

def buyer_screen():
    global inventory, worksheet, cart
    while True:
        for x, y in inventory.items():
            print(x, "$" + y)
        print (cart)
        cart_add = input('Add to cart Y/N :')
        if(cart_add == 'Y'):
            #Check sheet again after any changes by admin
            chosen_item = input('Which choice would you like? :')
            price = inventory[chosen_item]
            price = float(price)
            stock = (worksheet.col_values(3)[1:])
            supply = {items:stock for items, stock in zip(items, stock)}
            print('We currently have ', supply[chosen_item], ' in stock.')
            ammount = input('How many would you like? :')
            ammount = int(ammount)
            item_cell = worksheet.find(chosen_item)
            stock_row = item_cell.row
            up_stock = int(worksheet.cell(stock_row, 3).value) - ammount
            if(up_stock > 0):
                worksheet.update_cell(stock_row , 3, up_stock)
                ammount = float(ammount)
                cost = float (price * ammount)
                if (len(cart) == 0): #Seeing if cart is empty
                    cart.update({chosen_item: round(cost, 2)})
                elif(chosen_item in list(cart.keys())): #Seeing if the item chosen is already in the cart
                    cart[chosen_item] = cart[chosen_item] + cost
                else:
                    cart.update({chosen_item: round(cost, 2)})
                spacing()
            else:
                print('Sorry, we only have ', supply[chosen_item], ' left.')
                pass
        else:
            break
    grand_total = sum(cart.values())
    print('Your total is $', round(grand_total, 2))
    cart = {}

def admin_screen():
    global inventory, admin_direct
    password = input('What is the password? :')
    if (password == 'Password'):
        print('Please select an action', 'Add to Stock', 'Change Price', 'New Item', 'Delete Item', sep='\n')
        admin_direct = input('Select Action:')
    else:
        print('Incorrect Password')

def add_stock():
    global inventory
    added_item = input("Which items to add:")
    print("Current Stock:" + supply[added_item])
    added_inv = input('How many to add?')
    updated_stock = int(supply[added_item]) + int(added_inv)
    cell = worksheet.find(added_item)
    worksheet.update_cell(cell.row, 3, updated_stock)

def price_change():
    global inventory
    changed_item = input("Which item's price to change")
    changed_price = input('What is the new price?')
    cell = worksheet.find(changed_item)
    worksheet.update_cell(cell.row, 2, changed_price)

def brand_new():
    global inventory
    new_item = input('Add new item :')
    new_price = input('What is its price? :')
    new_stock = input('How many are there? :')
    new_row = [new_item, new_price, new_stock]
    worksheet.append_row(new_row)

def delete_item():
    global inventory
    item_to_delete = input('What item to delete?')
    cell = worksheet.find(item_to_delete)
    worksheet.delete_rows(cell.row)


while True:
    home_screen()
    if (direction == 'See Items'):
        spacing()
        buyer_screen()
        update_dictionaries()
    elif (direction == 'Admin Login'):
        spacing()
        admin_screen()
        if (admin_direct == 'Add to Stock'):
            add_stock()
        elif (admin_direct == 'Change Price'):
            price_change()
        elif (admin_direct == 'New Item'):
            brand_new()
        elif (admin_direct == 'Delete Item'):
            delete_item()
        else:
            spacing()
            print('Please select one of the options')
        update_dictionaries()
    else:
        spacing()
        print('Please select one of the options')
    spacing()

