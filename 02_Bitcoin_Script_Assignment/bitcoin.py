'''This eample is from https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line/blob/master/18_4_Accessing_Bitcoind_with_Python.md'''

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

from pprint import pprint
import logging

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = "bitcoin"
rpc_pass = "J9JkYnPiXWqgRzg3vAA"
rpc_host = "127.0.0.1"
rpc_client = AuthServiceProxy(f"http://{rpc_user}:{rpc_pass}@{rpc_host}:18332", timeout=120)

block_count = rpc_client.getblockcount()
print("---------------------------------------------------------------")
print("Block Count:", block_count)
print("---------------------------------------------------------------\n")

blockhash = rpc_client.getblockhash(block_count)
block = rpc_client.getblock(blockhash)

nTx = block['nTx']
if nTx > 10:
    it_txs = 10
    list_tx_heading = "First 10 transactions: "
else:
    it_txs = nTx
    list_tx_heading = f"All the {it_txs} transactions: "
print("---------------------------------------------------------------")
print("BLOCK: ", block_count)
print("-------------")
print("Block Hash...: ", blockhash)
print("Merkle Root..: ", block['merkleroot'])
print("Block Size...: ", block['size'])
print("Block Weight.: ", block['weight'])
print("Nonce........: ", block['nonce'])
print("Difficulty...: ", block['difficulty'])
print("Number of Tx.: ", nTx)
print(list_tx_heading)
print("---------------------")
i = 0
while i < it_txs:
    print(i, ":", block['tx'][i])
    i += 1
print("---------------------------------------------------------------\n")


wallet_info = rpc_client.getwalletinfo()
print("---------------------------------------------------------------")
print("Wallet Info:")
print("-----------")
pprint(wallet_info)
print("---------------------------------------------------------------\n")

tx_list = rpc_client.listtransactions()
pprint(tx_list)

print("Exploring UTXOs")
## List UTXOs
utxos = rpc_client.listunspent()
print("Utxos: ")
print("-----")
pprint(utxos)
print("------------------------------------------\n")

# Make a transaction

new_address = rpc_client.getnewaddress("Learning-Bitcoin-from-the-Command-Line")
new_change_address = rpc_client.getrawchangeaddress()

utxos = rpc_client.listunspent()
selected_utxo = utxos[0]  # again, selecting the first utxo here
utxo_address = selected_utxo['address']
utxo_txid = selected_utxo['txid']
utxo_vout = selected_utxo['vout']
utxo_amt = float(selected_utxo['amount'])

recipient_address = new_address
recipient_amt = utxo_amt / 2  # sending half coins to recipient
miner_fee = 0.00000300        # choose appropriate fee based on your tx size
change_address = new_change_address
change_amt = float('%.8f'%((utxo_amt - recipient_amt) - miner_fee))

txids_vouts = [{"txid": utxo_txid, "vout": utxo_vout}]
addresses_amts = {f"{recipient_address}": recipient_amt, f"{change_address}": change_amt}
unsigned_tx_hex = rpc_client.createrawtransaction(txids_vouts, addresses_amts)

address_priv_key = []  # list of priv keys of each utxo
address_priv_key.append(rpc_client.dumpprivkey(utxo_address))

signed_tx = rpc_client.signrawtransactionwithkey(unsigned_tx_hex, address_priv_key)

send_tx = rpc_client.sendrawtransaction(signed_tx['hex'])