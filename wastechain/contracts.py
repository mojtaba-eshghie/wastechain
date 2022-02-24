from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn
import json
import base64
from algosdk.mnemonic import to_private_key
from algosdk.transaction import AssetConfigTxn

"""
# to create an nft:
txn = AssetConfigTxn(sender=accounts[1]['pk'],
    sp=params,
    total=1,           
    default_frozen=False,
    unit_name="ALICEART",
    asset_name="Alice's Artwork@arc3",
    manager="",
    reserve="",
    freeze="",
    clawback="",
    url="https://path/to/my/nft/asset/metadata.json",
    metadata_hash=json_metadata_hash,
    decimals=0)        
"""


def wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait    
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return 
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:  
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)                   
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))


def generate_algorand_keypair():
    private_key, address = account.generate_account()
    #print("My address: {}".format(address))
    #print("My private key: {}".format(private_key))
    #print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))
    return (private_key, address)



def first_transaction_example(private_key, my_address):
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    algod_client = algod.AlgodClient(algod_token, algod_address)
    account_info = algod_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")


    """
    Creating the tx 
    """
    params = algod_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000
    receiver = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
    note = "Hello World".encode()

    unsigned_txn = PaymentTxn(my_address, params, receiver, 1000000, None, note)
    signed_txn = unsigned_txn.sign(private_key)
    print(signed_txn)


    """
    Sending the tx
    """
    txid = algod_client.send_transaction(signed_txn)
    print("Successfully sent transaction with txID: {}".format(txid))

    # wait for confirmation 
    try:
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))




# the following code is for generic account generation
#first_transaction_example(*generate_algorand_keypair())


# the following code I used for using known accounts with sufficient funds:
private_key = to_private_key("defense kite valid fancy choose matter arch island dish brass kid pigeon correct steak undo web glass rally gather airport endless season horror abandon ozone")
address = "JKHRVEXP3LAOG6YA5KWHH5WKX5UZERO7XM3A4RWGNB74O7PF6OMNBDHVBU"
first_transaction_example(private_key, address)




print(algod.algod_client)


params = algod.algod_client.suggested_params()


sample_hash = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# to create an nft:
txn = AssetConfigTxn(sender=address,
    sp=params,
    total=1,           
    default_frozen=False,
    unit_name="ALICEART",
    asset_name="Alice's Artwork@arc3",
    manager="",
    reserve="",
    freeze="",
    clawback="",
    url="https://path/to/my/nft/asset/metadata.json",
    metadata_hash=sample_hash,
    decimals=0) 


print(txn)