# A simple script to help you swipe all the assets from your Liquid wallet

## Installation

1. clone this repository
2. create a virtual env: `python3 -m venv venv`
3. activate: `. venv/bin/activate`
4. install requests: `pip install requests`
5. done!

This tool have been tested with Python 3.6.9, it should run fine with any version of Python3, still let us know if you encounter any issue.

## RPC configuration

The tool uses a very simple rpc client to make rpc call to elements-cli. You can find it in the `rpc.py` file.

First thing to do is to configure this file so that it can make calls to your own elements node.

If you are testing with regtest, set the `LIQUID_REG_1` variable to the http address of your own node. `rpc_user` and `rpc_password` are provided in the format `http://rpc_user:rpc_password@$URL:$PORT`. It is recommended not to make rpc calls in remote, so `$URL` should be `127.0.0.1`. All those informations can be found in the `elements.conf` file that should be in elements datadir (default is `$HOME/.elements`).

If you're on liquid mainnet, modify the `LIQUID` variable, and don't forget to toggle `CHAIN` and `POLICY_ASSET` to mainnet values in `swipe_assets.py`. 

The `CONF1` variable is not used for swiping assets.

## Running the tool

1. Make sure that elements is running and that the credentials and url provided in `rpc.py` are accurate.
2. Make sure to have at least one address to send each different asset. If you're not sure how many assets you really have you can go to step 3 first, the tool will tell you how many addresses it need, you can then abort and come back here. Copy each address in a text file, one address by line (i.e, each address separated by a new line in the file), and save the file in the tool directory.
3. still in the tool directory, `python3 swipe_assets.py`
4. You will see all your assets with the amounts of each printed on screen, and the program will prompt you for the file containing addresses (see step 2). Remember this file must be in the same directory.
5. Next you will see the arguments that will be send to elements for the `sendmany` command: addresses, assets and amounts. You can make sure that everything is fine and type `y` or `yes` to make the transaction, or any other key to abort.
6. Just wait for a confirmation or two, now your wallet should be totally empty

It is advised that you never delete a wallet, even if it's (supposedly) empty. You should remove it from the elements directory and back it up somewhere else with some straightforward, easy to figure out name like `elements_wallet-2020-09-12.dat`, restart elements and it should automatically create a new default wallet if it can't find the old one.

## Troubleshoot

* Remember that no matter what you need L-BTC to pay transaction fees. If you don't have any, you won't be able to move other assets.
* If possible, always do a test on regtest first and read the confirmation message before validation the transaction.
* There's a lot of room for improvement and there might be errors and bugs we didn't spot yet, so if someting's wrong please open an issue here and we will sure have a look.