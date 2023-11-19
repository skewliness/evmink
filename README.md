# 便宜Twitter令牌号：[hdd.cm](https://hdd.cm/)  单价低至0.2元

**适用于所有EVM链**

**适用于所有EVM链**

# 依赖：
```
pip install web3
pip install httpx
```


# 自动打包
右边Releases里打包好的exe是Github Action自动打包

打包脚本[.github/workflows/main.yml](.github/workflows/main.yml)

可以自行Fork仓库，自己去Action→发布软件→Run workflow

等待若干时间，会自动帮你打包好并发布到Releases。


# 使用教程

1. **输入地址**：这是你接收铭文的地址
2. **输入私钥**：付gas账号私钥
3. **输入RPC**：打哪个链用哪个链的RPC，有的RPC不支持batchRequest，多换几个
4. **输入是否EIP1559**：1159就是输入最大gasPrice，小费gasPrice那种，非1159就是直接输入gasPrice
5. **输入gasPrice**：就是gasPrice
6. **输入maxFeePerGas**：这个是最大gasPrice，可以多给点
7. **输入maxPriorityFeePerGas**：这个是小费gasPrice
8. **输入data**：支持直接复制铭文文本，或者十六进制（必须0x开头）

# 动态id
**动态id** 对于动态ID的，直接复制铭文文本：比如

```
data:,{"p":"bsc-20","op":"mint","tick":"bnbw","id":"1","amt":"1000"}
```

将里边变动的部分用方括号加范围：[开始值-结束值]，如[3242-8765]替换

```
data:,{"p":"bsc-20","op":"mint","tick":"bnbw","id":"[3242-8765]","amt":"1000"}
```

一定要注意只替换变动数字，不要替换其他的，如果有引号不要漏掉引号

   
# 其它说明

**输入的私钥账号可以和接收铭文账号不是同一个，也可以是同一个。不同就是小号给大号打，相同就是自转**

**请尽量不要使用大号私钥打，请为每个项目专门搞个小号，不论是直接双压卖私钥，还是卡交易都好处理**


一包100个，循环100次，理论上是会跑10000个，但是实际上会卡nonce，多跑几遍就是
