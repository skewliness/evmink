from web3 import AsyncWeb3
import httpx
import asyncio
import re


async def mint(to, rpc, private_key, gasPrice, maxFeePerGas, maxPriorityFeePerGas, data):
    web3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(rpc))
    account = web3.eth.account.from_key(private_key)
    http = httpx.AsyncClient()

    chain_id = await web3.eth.chain_id
    to = web3.to_checksum_address(to)
    nonce = await web3.eth.get_transaction_count(account.address)
    gasPrice = web3.to_wei(float(gasPrice), 'gwei')
    maxFeePerGas = web3.to_wei(float(maxFeePerGas), 'gwei')
    maxPriorityFeePerGas = web3.to_wei(float(maxPriorityFeePerGas), 'gwei')

    tx = {
        'from': account.address,
        'to': to,
        'nonce': nonce,
        'gas': 25024,
        'gasPrice': gasPrice,
        'maxFeePerGas': maxFeePerGas,
        'maxPriorityFeePerGas': maxPriorityFeePerGas,
        'chainId': chain_id,
        'data': data
    }

    if gasPrice == 0:
        del tx['gasPrice']
    else:
        del tx['maxFeePerGas']
        del tx['maxPriorityFeePerGas']

    match = re.search(r'\[(\d+)-(\d+)\]', data)
    if match:
        start, end = map(int, match.groups())
        subtext = match.group()
    else:
        start, end, subtext = 0, 0, None

    time = (end - start) // 100 + 1 if end - start > 10000 else 100

    if not data.startswith('0x') and subtext is None:
        data = web3.to_hex(text=data)

    for x in range(0, time):
        request_list = []
        for i in range(0, 100):
            tx['nonce'] = nonce
            if subtext is not None:
                tx['data'] = data.replace(subtext, str(start))
                start += 1
                if start > end:
                    print('已经到达最大范围')
                    return
            signed = account.sign_transaction(tx)
            nonce += 1
            request_list.append({"jsonrpc": "2.0", "method": "eth_sendRawTransaction", "params": [signed.rawTransaction.hex()], "id": i + 1})
        res = await http.post(rpc, json=request_list)
        print(res.json())
        await asyncio.sleep(1)


def get_input(prompt, check, error_msg):
    while True:
        data = input(prompt).strip()
        if check(data):
            return data.strip()
        else:
            print(error_msg)


async def main():
    _to = get_input('输入地址(打到那个号)：', lambda addr: len(addr) == 42, '地址长度不对, 请检查后重新输入')
    _private_key = get_input('输入私钥(有gas的小号)：', lambda key: len(key) == 64 or (key.startswith('0x') and len(key) == 66), '私钥长度不对, 请检查后重新输入')

    _rpc = get_input('输入RPC：', lambda rpc: rpc.startswith('https://'), 'RPC格式不对, https://开头, 请检查后重新输入')
    _eip1559 = get_input('输入是否EIP1559(1为是，0为否)：', lambda eip1559: eip1559 in ['0', '1'], '输入错误, 必须为0或1, 请检查后重新输入')

    if _eip1559 == '1':
        _gasPrice = 0
        _maxFeePerGas = get_input('输入maxFeePerGas：', lambda maxFeePerGas: float(maxFeePerGas) > 0, 'maxFeePerGas必须大于0, 请检查后重新输入')
        _maxPriorityFeePerGas = get_input('输入maxPriorityFeePerGas：', lambda maxPriorityFeePerGas: True, 'maxPriorityFeePerGas必须大于0, 请检查后重新输入')
    else:
        _gasPrice = get_input('输入gasPrice：', lambda gasPrice: float(gasPrice) > 0, 'gasPrice必须大于0, 请检查后重新输入')
        _maxFeePerGas = 0
        _maxPriorityFeePerGas = 0

    _data = get_input('输入data：', lambda data: len(data) > 0, 'data不能为空, 请检查后重新输入')

    await mint(_to, _rpc, _private_key, _gasPrice, _maxFeePerGas, _maxPriorityFeePerGas, _data)


if __name__ == '__main__':
    print('hdd.cm, 推特低至2毛，一手资源，售后无忧')
    print('https://github.com/Fooyao/evmink; 请仔细阅读README文档')
    asyncio.run(main())
