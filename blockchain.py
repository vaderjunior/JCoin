from datetime import datetime
import hashlib
import json
from flask import Flask
from flask import jsonify
from time import time

class Block():

    def __init__(self,nonce,tstamp,tlist,prevhash='',hash=''):
        self.nonce=nonce
        self.tstamp=tstamp
        self.tlist=tlist
        self.prevhash=prevhash
        self.hash=self.calcHash()

        if(hash==''):
                self.hash=self.calcHash()

        else:
            self.hash=hash

    def calcHash(self):
        block_string=json.dumps({"none":self.nonce,"tstamp":str(self.tstamp),"tlist":self.tlist,"prevhash":self.prevhash},sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mineBlock(self,difficulty):
        while(self.hash[:difficulty]!=str('').zfill(difficulty)):
            self.nonce+=1
            self.hash=self.calcHash()
        #print("Block mined",self.hash)

    def toDict(self):
        return {"nonce":self.nonce,"tstamp":str(self.tstamp),"tlist":self.tlist,"prevhash":self.prevhash,"hash":self.hash}

class Blockchain():

    def __init__(self):
        self.chain=[]
        self.difficulty=3
        self.generateGenesisBlock()
        self.pendingTransaction=[]
        self.mining_reward=100

    def generateGenesisBlock(self):
        dict={"nonce":0,"tstamp":'02/02/2019',"tlist":[{"from_add":None,"to_add":None,"amount":0},],"hash":""}
        b=Block(**dict)
        self.chain.append(b.toDict())

    def getLastBlock(self):
        return Block(**self.chain[-1])
    
    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        
        max_length = len(self.chain)

        
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

        
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def minePendingTransaction(self,mining_reward_address):
        block=Block(0,str(datetime.now()),self.pendingTransaction)
        block.prevhash=self.getLastBlock().hash
        block.mineBlock(self.difficulty)
        print("Block is mined, the reward is"+str(self.mining_reward))
        self.chain.append(block.toDict())
        self.pendingTransaction=[{"from_add":None,"to_add":mining_reward_address,"amount":self.mining_reward},]

    def createTransaction(self,from_add,to_add,amount):
        self.pendingTransaction.append({'from_add':from_add,'to_add':to_add,'amount':amount})

    def  getBalance(self,address):
        balance=0
        for index in range(len(self.chain)):
            dictList=self.chain[index]["tlist"]
            for dic in dictList:

                if dic["to_add"]==address:
                    balance+=t.amount

                if dic["from_add"]==address:
                    balance-=t.amount
        return balance

    def isChainValid(self):
        for i in range(1,len(self.chain)):

            if(Block(**self.chain[i]).hash!=Block(**self.chain[i]).calcHash()):
                print("invalid block"+"/n")
                return False

            if(Block(**self.chain[i-1]).hash!=Block(**self.chain[i]).prevhash):
                print("invalid chain"+"/n")
                return False
        return True

JCoin=Blockchain()
num=int(input('Enter the number of nodes'))
while(num>0):
    num-=1
    a1=str(input())
    a2=str(input())
    amount=int(input())
    mining_add=str(input())
    JCoin.createTransaction(a1,a2,amount)

    JCoin.minePendingTransaction(mining_add)
    JCoin.minePendingTransaction(None)

JCoin.createTransaction('None','address1',100)
JCoin.createTransaction('address1','address2',100)
JCoin.createTransaction('address2','address1',50)
print("Starting mining")
JCoin.minePendingTransaction("mining_add")


print("Miner bal is "+str(JCoin.getBalance('mining_add')))
print(JCoin.isChainValid())

app=Flask(__name__)
@app.route("/mine",methods=['GET'])
def mine():
    a1=str(input())
    a2=str(input())
    amount=int(input())
    mining_add=str(input())
    JCoin.createTransaction(a1,a2,amount)

    JCoin.minePendingTransaction(mining_add)
    JCoin.minePendingTransaction('System'

    print("Miner bal is " + str(JCoin.getBalance(mining_add)))
    print(JCoin.isChainValid())
    return "we are going to mine the block with new transactions here"

@app.route('/transactions/new',methods=['POST'])
def new_transaction():
    return None
@app.route("/chain",methods=['GET'])
def display_full_chain():
    response={
        'chain':JCoin.chain,
        'length':len(JCoin.chain)
    }
    return jsonify(response),200
@app.route("/")
def hello():
    return "Hello you are in the main page of this node"
if __name__=="__main__":
    app.run()
