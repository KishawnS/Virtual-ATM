from random import randint

#Account Class
class Account:
  def __init__(self, number, name, pin, balance = 0.0):
    self.number = number
    self.name = name
    self.pin = pin
    self.balance = balance

  def getNumber(self):
    return self.number

  def getName(self):
    return self.name

  def getPin(self):
    return self.pin

  def getBalance(self):
    return self.balance

  def withdraw(self, amount):
    if (self.balance >= amount):
      self.balance -= amount
      print("$%.2f has been withdrawed." % amount)
    else:
      print("Insufficient balance in account.")

  def deposit(self, amount):
    self.balance += amount
    print("$%.2f has been deposited." % amount)

  def transfer(self, amount, recipient):
    if (self.balance >= amount):
      self.balance -= amount
      recipient.balance += amount
      print("$%.2f has been transferred to %s." % (amount, recipient.getName()))
    else:
      print("Insufficient balance in account.")

  def changeName(self, newName):
    self.name = newName
    print("Name succesfully changed.")

  def changePin(self, currentPin, newPin):
    if (currentPin == self.pin):
      self.pin = newPin
      print("Pin successfully changed.")
    else:
      print("Incorrect current pin. Pin cannot be changed.")
      
#Updating Accounts File
def saveAccounts(accounts):
  accountsFile = open("accounts.txt", "w")
  accountsFile.write("Account Number | Client Name | Pin | Account Balance\n")
  accountsFile.close()
  accountsFile = open("accounts.txt", "a")
  for account in accounts:
    accountsFile.write(str(account.getNumber())+" | "+account.getName()+" | "+str(account.getPin())+" | "+str(account.getBalance())+"\n")
  accountsFile.close()

#Account Display
def accountOptions(account):
  print("\nAccount: %d" % account.getNumber())
  print("Client: %s" % account.getName())
  print("\n1. Withdrawal")
  print("2. Deposit")
  print("3. Transfer Funds")
  print("4. View Account Balance")
  print("5. Change Legal Name")
  print("6. Change Pin")
  print("7. Close Account Permanently\n")
  transaction = int(input("Enter transaction option number (0 to end session): "))
  return transaction

#Opening New Account
def newAccount(accounts):
  number = randint(1000000, 9999999)    
  name = input("Enter your name: ")
  pin = int(input("Set your pin: "))
  return Account(number, name, pin)

#Loading Accounts File to Local List
accounts = []
accountsFile = open("accounts.txt", "r")
accountsFile.readline()
for line in accountsFile:
  tempAccount = line.split(" | ")
  loadAccount = Account(int(tempAccount[0]), tempAccount[1], int(tempAccount[2]), float(tempAccount[3]))
  accounts.append(loadAccount)
accountsFile.close()

#ATM Program
while True:
  accountType = input("Do you have an existing bank account (Y/N)? ")

  #Accessing Existing Account 
  if (accountType == "Y"):
    accountNum = int(input("\nEnter your bank account number: "))
    wrongNum = True
    for account in accounts:
      if (account.getNumber() == int(accountNum)):
        wrongNum = False
        for i in range(3, -1, -1):
          pin = int(input("\nEnter your pin: "))
          if (pin != account.getPin()):
            print("Wrong pin. %d tries remaining." % i)
          else:
            break
        if (pin == account.getPin()):
          transaction = accountOptions(account)
          if (transaction == 0):
            print("\nSession ended.\n")
          while (transaction != 0):
            if (transaction == 1):
              withdrawal = float(input("\nWithdrawal Amount: $"))
              account.withdraw(withdrawal)
            elif (transaction == 2):
              deposit = float(input("\nDeposit Amount: $"))
              account.deposit(deposit)
            elif (transaction == 3):
              recipient = int(input("\nEnter account number of recipient: "))
              accountFound = False
              for receiver in accounts:
                if (receiver.getNumber() == recipient):
                  accountFound = True
                  fund = float(input("Transfer Amount: $"))
                  account.transfer(fund, receiver)
              if (accountFound == False):
                print("Recipient account does not exist.")
            elif (transaction == 4):
              print("\nBalance: $%.2f" % account.getBalance())
            elif (transaction == 5):
              newName = input("\nEnter new name: ")
              account.changeName(newName)
            elif (transaction == 6):
              currentPin = int(input("\nEnter your current pin: "))
              newPin = int(input("Set your new pin: "))
              account.changePin(currentPin, newPin)
            elif (transaction == 7):
              print("\nAccount #%d has been closed permanently." % account.getNumber())
              accounts.remove(account)
              saveAccounts(accounts)
              print("\nSession ended.\n")
              break
            else:
              print("\nEnter valid transaction option.")
            saveAccounts(accounts)
            transaction = accountOptions(account)
            if (transaction == 0):
              print("\nSession ended.\n")
        else:
          print("\nTry again later.\n")
    if (wrongNum):
      print("\nEnter a valid account number.\n")

  #Opening New Account
  elif (accountType == "N"):
    print("\nWelcome to the bank!\nCongratulations, you have qualified to open a new bank account with us.\n")
    currentAccount = newAccount(accounts)
    print("\n%s, your new account number is %d.\n" % (currentAccount.getName(), currentAccount.getNumber()))
    accounts.append(currentAccount)
    saveAccounts(accounts)

  else:
    print("\nPlease enter a valid response.\n")