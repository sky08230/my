import logging

# set up the logger file 
logging.basicConfig(filename='log_bank.csv',filemode='w+',format='%(asctime)s -%(name)s -%(levelname)s -%(message)s')
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BankingSystemImp:
    """
    create banksystem class to perform functions create account, withdraw, deposit and transfer.
    """
    #initialize the class with account data dictionary
    def __init__(self):
        self.account={}

    # function to create account    
    def create_account(self, name, balance=0):
        if name in self.account.keys():
            logger.error("%s already exist",name)
            return False
         
        else:
            self.account[name]=balance
            logger.info("successfully create account %s with %s", name, balance)
            return self.account[name]

     # function to deposit money for account        
    def deposit(self, name, amount):
        if name not in self.account.keys():
            logger.error("%s not exist in the system",name)
            return False
        else:
            self.account[name]=amount+self.account[name]
            logger.info("successfully deposit account %s with %s", name, amount)
            return self.account[name]
        
    # function to witdraw money for account        
    def withdraw(self, name, amount):
        if name not in self.account.keys():
            logger.error("%s not exist in the system",name)
            return False
        #check if the money is enough 
        elif self.account[name]< amount:
            logger.error("overdraft account")
            return False       
        else:
             self.account[name]=self.account[name]-amount
             logger.info("successfully withdraw account %s with %s", name, amount)
             return self.account[name]
        
    # function to transfer money for account              
    def transfer(self, source_account, target_account, amount):
        if source_account not in self.account.keys() or target_account not in self.account.keys():
            logger.error("account not exist in the system")
            return False
        elif self.account[source_account]<amount:
            logger.error("overdraft account")
            return False
        else:  
            self.account[source_account]=self.account[source_account]-amount
            self.account[target_account]=self.account[target_account]+amount
            logger.info("successfully transfer from %s to %s with %s", source_account,target_account, amount)
            return self.account[source_account],self.account[target_account]


     

                  
            
     
        
            
                       
             


