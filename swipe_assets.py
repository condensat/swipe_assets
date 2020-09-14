import logging
import rpc
from sys import exit
from os import getcwd

#CHAIN = 'liquid'
CHAIN = 'elements-regtest'
POLICY_ASSET = 'b2e15d0d7a0c94e4e2ce0fe6e8691b9e451377f6e46e8045a86f7c4b5d4f0f23'
#POLICY_ASSET = '6f0279e9ed041c3d710a9f57d0c02928416460c4b722ae3457a11eec381c526d'

def btc2sat(btc):
  return round(btc * 10**8)

def sat2btc(sat):
  return round(sat * 10**-8, 8)

def list_assets(r):
  assets = {}
  res = r.call('listunspent', 0)
  for utxo in res:
    if utxo['asset'] in assets:
      asset = utxo['asset']
      amount = btc2sat(assets[asset]) + btc2sat(utxo['amount'])
      assets[asset] = sat2btc(amount)
    else:
      asset = utxo['asset']
      amount = btc2sat(utxo['amount'])
      assets[asset] = sat2btc(amount)
  return assets

def get_addresses(num):
  dest_addr = []
  file = ""
  file = input(f"""
                Please provide a filename in the same dir 
                with {num} addresses, one by line:\n
                """)
  with open(getcwd() + "/" + file, 'r') as f:
    content = f.read()
    dest_addr = content.splitlines()
  return dest_addr

def map_addr_amount(addresses, assets):
  """
  Map the addresses with the amount we send to each of them
  """
  addr2amt = {}
  assets_cpy = assets.copy()
  for n, asset in enumerate(assets):
    addr2amt[addresses[n]] = assets_cpy.pop(asset)
  # return a dict with addr and amt
  return addr2amt

def map_addr_asset(addr2amt, assets):
  # got a dict of addr: amt and a dict asset: amt
  # we should take the first dict and just modify the value with the asset
  # and control that the asset is coherent with the amount
  addr2asset = addr2amt.copy()
  for addr in addr2asset:
    for asset in assets:
      if addr2asset[addr] == assets[asset]:
        addr2asset[addr] = asset
      else:
        continue
  # return a dict with addr and asset
  return addr2asset

def get_lbtc_address(addr2asset):
  for addr in addr2asset:
    logging.debug(f"{addr2asset[addr]}")
    if addr2asset[addr] == POLICY_ASSET:
      return [addr]
  logging.error("No LBTC found, please send some LBTC to pay fees")
  return ""

def swipe_assets():
  from collections import namedtuple

  r = rpc.RPCHost(CHAIN)
  assets = {}
  change_addr = []
  logging.info(f"swipe_assets chain: {CHAIN}")
  logging.info(f"listing all utxos")
  assets = list_assets(r)
  logging.info(f"listing all LBTC addresses")
  for asset in assets:
    logging.debug(f"{asset} : {assets[asset]}")

  # get the destination addresses, one by asset
  dest_addr = get_addresses(len(assets))

  # create a dict for dest address: amount
  addr2amt = map_addr_amount(dest_addr, assets)

  # create a dict for address: asset
  addr2asset = map_addr_asset(addr2amt, assets)

  # take the address that get LBTC to pay the fees
  pay_fee_addr = get_lbtc_address(addr2asset)
  if not pay_fee_addr:
    exit()

  # wrap it up and make a sendmany call
  Args = namedtuple('args', 'dummy amounts minconf comment \
    substractfeefrom replaceable conf_target estimate_mod output_assets')
  params = Args("", addr2amt, 1, "wallet cleanup", pay_fee_addr, False, 6, 'UNSET', addr2asset)
  if (input(f"please confirm you want to do sendmany with the following arguments: \n{params}\n")) in ['y', 'yes']:
    txid = r.call("sendmany", *params)
    return txid
  else:
    logging.info("swipe aborted by user\n")
    exit()
  
if __name__ == "__main__":
  import logger
  logger.setup(logger.Args('debug'))

  # wipe all utxos to new addresses
  txid = swipe_assets()
  if not txid:
    print("Something is wrong\n")
  else:
    print(txid)
  # make a dump of the wallet.dat
  # stop the elements service
  # move wallet.dat to wallet.$m.$d
  # restart elements service
