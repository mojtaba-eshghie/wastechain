from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import PaymentTxn
import json
import base64
from algosdk.mnemonic import to_private_key
from algosdk.future.transaction import AssetConfigTxn

print("starting to run the algorand application")

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

"""
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)
params = algod_client.suggested_params()
print(params)
"""

private_key = to_private_key("tide syrup cannon sick lend trophy coast bottom doctor recycle extra option typical shed nose team general patch blossom wood again mountain pizza about access")
address = "QNWYDABSRUSNAMUEZPLWORIRWNHRHDYT677XR3V5LBY5BZPHULWMMP6TOI"

print('just retreived my private key!!!! and it is: {}'.format(private_key))

algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)

print('The algorand client: {}'.format(algod_client))

params = algod_client.suggested_params()
sample_hash = b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'


print('Creating the tx configs')

# to create an nft:
txn = AssetConfigTxn(sender=address,
    sp=params,
    total=100,    
    default_frozen=False,
    unit_name="unit0",
    asset_name="Alice's Artwork@arc3",
    manager=address,
    reserve=None,
    freeze=None,
    clawback=None,
    strict_empty_address_check=False,
    url="https://path/to/my/nft/asset/metadata.json",
    metadata_hash=sample_hash,
    decimals=0) 

print("Assigned the configuration of transaction")

stxn = txn.sign(private_key)

print("Signed the tx")

# Send the transaction to the network and retrieve the txid.
txid = algod_client.send_transaction(stxn)
print("Asset Creation Transaction ID: {}".format(txid))