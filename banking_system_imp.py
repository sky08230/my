import logging
from collections import defaultdict

# set up the logger file 
logging.basicConfig(filename='log_bank.csv',filemode='w+',format='%(asctime)s -%(name)s -%(levelname)s -%(message)s')
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)



class BankingSystemImpl:

    def __init__(self):
        self.account=[]
        self.balance={}
        self.transf=defaultdict(lambda :0)
        self.cashback=[]
        self.payid=0
        
    def cashback(fun):
        def call(self,*args):
            for item in self.cashback:
                if self.cashback!=[] and item[0]<=args[0]:
                    self.cashback.remove(item)
                    self.deposit(args[0],item[1],item[2])
            return fun(self,*args)                        
        return call
                          
        
    @cashback    
    def create_account(self, timestamp: int, account_id: str):
        if account_id in self.account:
            return False
        else:
            self.account.append(account_id)  
            self.balance[account_id]=0
            self.transf[account_id]=0
            return True
        
    @cashback    
    def deposit(self, timestamp: int, account_id: str, amount: int):
        if account_id not in self.account:
            return None
        else:
            self.balance[account_id]=amount+self.balance[account_id]
            return self.balance[account_id]
    @cashback        
    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int):
        if source_account_id not in self.account or target_account_id not in self.account:
            return None
        elif  source_account_id== target_account_id:
            return None
        elif self.balance[source_account_id]<amount:
            return None
        else:  
            self.transf[source_account_id]=self.transf[source_account_id]+amount
            self.balance[source_account_id]=self.balance[source_account_id]-amount
            self.balance[target_account_id]=self.balance[target_account_id]+amount
            return self.balance[source_account_id]
    @cashback
    def top_spenders(self, timestamp: int, n: int):
        rank=sorted(self.account,key=lambda k:self.transf[k],reverse=True)
        return rank[:n]
        
    @cashback
    def pay(self, timestamp: int, account_id: str, amount: int):
        if account_id not in self.account:
            return None
        elif self.balance[account_id]< amount:
            return None
        else:
            self.balance[account_id]=self.balance[account_id]-amount
            self.transf[account_id]=self.transf[account_id]+amount
            self.cashback.append([timestamp+86400000,account_id,0.02*amount])
            self.payid+=1
            return 'payment'+str({self.payid})+'succesfully'

     

                  
            
     
        
            
                       
             


