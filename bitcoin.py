from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

from pprint import pprint
import logging
#server = 1
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

#rpcauth=bitcoin:597e462228284010a9d35b23816eacf5$8f7b3695f938d046c44be0f4c056ab0a24ec8bb7e5dbbefb8eb5ab8f9aee7319