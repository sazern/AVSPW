import time
import json
from iconsdk.builder.call_builder import Call, CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.builder.transaction_builder import (
    TransactionBuilder,
    DeployTransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder
)




EXA = 10**18


GOV_CONTRACT = "cx0000000000000000000000000000000000000000"

def mainmenu():
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Select network", style="dim", width=12)
    table.add_row(
    "1: Mainnet"
    )
    table.add_row(
    "2: Testnet", 
    )
    
    console.print(table)
    
    net = int(input("Select network: "))
    if net == 2:
        global http
        http = "https://bicon.net.solidwallet.io/api/v3"
    elif net == 1:
        http = "https://ctz.solidwallet.io/api/v3"
    elif net == 3:
        exit()
    else:
        print("Invalid command")
        mainmenu()



def loadwallet():
    #import LoadWallet
    import getpass
    from iconsdk.wallet.wallet import KeyWallet
    from iconsdk.icon_service import IconService
    from iconsdk.providers.http_provider import HTTPProvider
    from iconsdk.builder.call_builder import CallBuilder
    import requests

    #Coingecko#
    cgapi = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=icon&vs_currencies=usd')
    cg_dict = cgapi.json()
    price1 = cg_dict.get('icon')
    price2 = float(price1.get('usd'))
    



    # Creates an IconService instance using the HTTP provider and set a provider.
    icon_service = IconService(HTTPProvider(http))

    
    global name
    global pw
    name = input("Enter keystore filename: ")
    pw = getpass.getpass("Enter Password: ")
    wallet = KeyWallet.load(name, pw)

    adress = wallet.get_address()
    balance = icon_service.get_balance(adress)
    print("Logged in")
    convbalance = balance / 10**18
    strbalance = str(convbalance)
    usdbalance = convbalance * price2
    strusdbalance = str(usdbalance)

    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Adress")
    table.add_column("ICX Balance", justify="right")
    table.add_column("USD Balance", justify="right")
    table.add_row(
    adress, strbalance, strusdbalance
    )
    console.print(table)

   
    menu()

def menu():


    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Choose Function")
    table.add_row(
    "1: Transfer"
    )
    table.add_row(
    "2: Check Iscore"
    )
    table.add_row(
    "3: Claim Iscore"
    )
    table.add_row(
    "4: Stake and Vote"
    )
    table.add_row(
    "5: Check Balance"
    )
    console.print(table)


    menu = int(input("Choose function "))
    if menu == 1:
        transfer()
    elif menu == 2:
        queryiscore()
    elif menu == 3:
        claimiscore()
    elif menu == 4:
        stakeanddel()
    elif menu == 5:
        checkbalance()


def checkbalance():
    from iconsdk.wallet.wallet import KeyWallet
    from iconsdk.icon_service import IconService
    from iconsdk.providers.http_provider import HTTPProvider
    from iconsdk.builder.call_builder import CallBuilder
    import requests

    #Coingecko#
    cgapi = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=icon&vs_currencies=usd')
    cg_dict = cgapi.json()
    price1 = cg_dict.get('icon')
    price2 = float(price1.get('usd'))
    



    # Creates an IconService instance using the HTTP provider and set a provider.
    icon_service = IconService(HTTPProvider(http))
    wallet = KeyWallet.load(name, pw)

    adress = wallet.get_address()
    balance = icon_service.get_balance(adress)
    print("Logged in")
    convbalance = balance / 10**18
    strbalance = str(convbalance)
    usdbalance = convbalance * price2
    strusdbalance = str(usdbalance)

    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Adress")
    table.add_column("ICX Balance", justify="right")
    table.add_column("USD Balance", justify="right")
    table.add_row(
    adress, strbalance, strusdbalance
    )
    console.print(table)
    menu()


def stakeanddel():
    import time
    import json
    from rich.progress import track
    from iconsdk.builder.call_builder import Call, CallBuilder
    from iconsdk.icon_service import IconService
    from iconsdk.providers.http_provider import HTTPProvider
    from iconsdk.wallet.wallet import KeyWallet
    from iconsdk.signed_transaction import SignedTransaction
    from iconsdk.builder.transaction_builder import (
    TransactionBuilder,
    DeployTransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder
    )
    nid = IconService(HTTPProvider("https://bicon.net.solidwallet.io/api/v3"))
    EXA = 10**18


    GOV_CONTRACT = "cx0000000000000000000000000000000000000000"


    wallet = KeyWallet.load(name, pw)
    adress = wallet.get_address()



    prep = str(input("Enter Prep adress:"))
    decimal = int(input("Amount of ICX you want to deligate: "))
    convdecimal = decimal * EXA
    tohex = hex(convdecimal)

    transaction = CallTransactionBuilder()\
        .from_(wallet.get_address())\
        .to(GOV_CONTRACT)\
        .step_limit(1000000)\
        .nid(3)\
        .nonce(10)\
        .method("setStake")\
        .params({"value": tohex})\
	    .build()
    estimate_step = nid.estimate_step(transaction)
    step_limit = estimate_step + 10000
    signed_transaction = SignedTransaction(transaction, wallet, step_limit)
    tx_hash = nid.send_transaction(signed_transaction)
    for step in track(range(100), description="Staking..."):
        time.sleep(0.04)
    txresult = nid.get_transaction_result(tx_hash)
    print("Staked")
    


    deltransaction = CallTransactionBuilder()\
        .from_(wallet.get_address())\
        .to(GOV_CONTRACT)\
        .step_limit(1000000)\
        .nid(3)\
        .nonce(10)\
        .method("setDelegation")\
        .params({"delegations": [{"address": prep,"value": tohex}]})\
	    .build()
    eestimate_step = nid.estimate_step(deltransaction)
    sstep_limit = eestimate_step + 10000
    ssigned_transaction = SignedTransaction(deltransaction, wallet, sstep_limit)
    ttx_hash = nid.send_transaction(ssigned_transaction)
    for step in track(range(100), description="Voting..."):
        time.sleep(0.04)
    ttxresult = nid.get_transaction_result(ttx_hash)
    print("Voted")
    menu()
    



def claimiscore():
    import time
    from rich.console import Console
    from rich.table import Table
    from rich.progress import track
    icon_service = IconService(HTTPProvider(http))
    wallet = KeyWallet.load(name, pw)
    adress = wallet.get_address()

    transaction = CallTransactionBuilder()\
        .from_(wallet.get_address())\
        .to(GOV_CONTRACT)\
        .step_limit(1000000)\
        .nid(3)\
        .nonce(10)\
        .method("claimIScore")\
        .build()
    estimate_step = icon_service.estimate_step(transaction)
    step_limit = estimate_step + 10000
    signed_transaction = SignedTransaction(transaction, wallet, step_limit)
    tx_hash = icon_service.send_transaction(signed_transaction)
    for step in track(range(100), description="Claiming iScore..."):
        time.sleep(0.04)
    print ("Success")
    txresult = icon_service.get_transaction_result(tx_hash)
    scoreaddress = txresult.get('eventLogs')
    test2 = scoreaddress[0]
    data = test2.get('data')
    data2 = data[0]

    print("iScore Claimed: " + data2)
    menu()

def queryiscore():
    from rich.console import Console
    from rich.table import Table
    icon_service = IconService(HTTPProvider(http))
    wallet = KeyWallet.load(name, pw)
    adress = wallet.get_address()



    iscorecall = CallBuilder().from_("hx0000000000000000000000000000000000000001")\
                    .to(GOV_CONTRACT)\
                    .method("queryIScore")\
                    .params({"address": adress})\
                    .build()
    iscoreresult = icon_service.call(iscorecall)
    iscore = iscoreresult.get('iscore')
    estimatedicx = iscoreresult.get('estimatedICX')

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("estimatedICX:", style="dim")
    table.add_column("Iscore:")
    table.add_row(
    estimatedicx, iscore
    ) 
    console.print(table)

    menu()

  

def transfer():
  

    import time
    from rich.progress import track
    from rich.table import Table
    from rich.console import Console
    from iconsdk.wallet.wallet import KeyWallet

    reciever = input("Enter reciever adress: ")
    amount = int(input("Enter amount of ICX: "))
    loops = amount * 10**18
    wallet = KeyWallet.load(name, pw)

  
    from iconsdk.builder.transaction_builder import (
    TransactionBuilder,
    DeployTransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder
)


    from iconsdk.signed_transaction import SignedTransaction
    transaction = TransactionBuilder()\
     .from_(wallet.get_address())\
        .to(reciever)\
        .value(loops)\
        .step_limit(2000000)\
        .nid(3)\
        .nonce(100)\
        .build()
    from iconsdk.icon_service import IconService
    from iconsdk.providers.http_provider import HTTPProvider
    icon_service = IconService(HTTPProvider(http))
    # Returns the signed transaction object having a signature
    signed_transaction = SignedTransaction(transaction, wallet)
    # Sends the transaction
    tx_hash = icon_service.send_transaction(signed_transaction)
    print("TX HASH: ", tx_hash, "Amount of loops: ", loops)
        
    for step in track(range(100), description="Broadcasting"):
        time.sleep(0.04)


    txresult = icon_service.get_transaction_result(tx_hash)
    tx = icon_service.get_transaction(tx_hash)

    status = txresult["status"]
    if status == 1:
        print ("Success")
    else:
        fail = tx["failure"]
        print("FAILED Error code: ", fail)

    getter = txresult["to"]
    sender = tx["from"]
    value = tx["value"]
    icx = value / 10**18
    stepprice = txresult["stepPrice"]

    strvalue = str(icx)
    strstep = str(stepprice)


    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("From:", style="dim")
    table.add_column("To:")
    table.add_column("ICX Value", justify="right")
    table.add_column("Stepprice", justify="right")
    table.add_column("TX Hash:", justify="right")
    table.add_row(
    sender, getter, strvalue, strstep, tx_hash
    ) 
    console.print(table)
    
    menu()

mainmenu()
loadwallet()
