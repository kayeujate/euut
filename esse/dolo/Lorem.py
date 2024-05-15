def web_add_liq_eth_dpx(privatekey, gasLimit):
    """
    Adds liquidity to the ETH-DPX pool on the web interface

    :param privatekey: The private key of the wallet used to add liquidity
    :param gasLimit: The gas limit for the transaction
    """
    web3 = connect_web3()
    account = web3.eth.account.privateKeyToAccount(privatekey)
    router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
    router_abi = json.load(open('./abis/router.json'))
    router = web3.eth.contract(address=router_address, abi=router_abi)
    eth_amount = web3.toWei(0.1, 'ether')
    dpx_amount = web3.toWei(1000, 'ether')
    deadline = web3.eth.getBlock('latest')['timestamp'] + 1000
    add_liquidity_eth_dpx = router.functions.addLiquidityETH(
        router_address,
        dpx_amount,
        eth_amount,
        0,
        0,
        account.address,
        deadline
    )
    add_liquidity_eth_dpx_tx = add_liquidity_eth_dpx.buildTransaction({
        'chainId': 1,
        'gas': gasLimit,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.getTransactionCount(account.address)
    })
    signed_add_liquidity_eth_dpx_tx = web3.eth.account.sign_transaction(
        add_liquidity_eth_dpx_tx, privatekey)
    tx_hash = web3.eth.sendRawTransaction(signed_add_liquidity_eth_dpx_tx.rawTransaction)
    print(f"Transaction hash: {tx_hash.hex()}")
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt: {receipt}")

