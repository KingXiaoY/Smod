import os
import threading

from System.Core.Global import *
from System.Core.Colors import *
from System.Core.Modbus import *
from System.Lib import ipcalc

class Module:


	info = {
		'Name': 'Read Coils Function',
		'Author': ['@enddo'],
		'Description': ("Fuzzing Read Coils Function"),

        }
	options = {
		'RHOSTS'	:['192.168.0.2'		,True	,'The target address range or CIDR identifier'],
		'RPORT'		:[502		,False	,'The port number for modbus protocol'],
		'UID'		:[1		,True	,'Modbus Slave UID.'],
		'StartAddr'	:['0x0000'	,True	,'Start Address.'],
		'Quantity'	:['0x0001'	,True	,'Registers Values.'],
		'Threads'	:[1		,False	,'The number of concurrent threads'],
		'Output'	:[True		,False	,'The stdout save in output directory']
	}	
	output = ''

	def exploit(self):

		moduleName 	= self.info['Name']
		print bcolors.OKBLUE + '[+]' + bcolors.ENDC + ' Module ' + moduleName + ' Start'
		ips = list()
		ip = ''
		for ip in ipcalc.Network(self.options['RHOSTS'][0]):
			ips.append(str(ip))
		while ips:
			for Quantity in [2243]:
				for StartAddr in range(2, 256):
					for i in range(int(self.options['Threads'][0])):
						if(len(ips) > 0):
								# print type(ips.pop(0))
								if Quantity == 255:
									thread = threading.Thread(target=self.do, args=(ips.pop(0),str(StartAddr),str(Quantity)))
								thread = threading.Thread(target=self.do, args=(str(ip),str(StartAddr),str(Quantity)))
								thread.start()
								THREADS.append(thread)
						else:
							break
					for thread in THREADS:
						thread.join()
				time.sleep(1.5)
		if(self.options['Output'][0]):
			open(mainPath + '/Output/' + moduleName + '_' + self.options['RHOSTS'][0].replace('/','_') + '.txt','a').write('='*30 + '\n' + self.output + '\n\n')
		self.output 	= ''

	def printLine(self,str,color):
		self.output += str + '\n'
		if(str.find('[+]') != -1):
			print str.replace('[+]',color + '[+]' + bcolors.ENDC)
		elif(str.find('[-]') != -1):
			print str.replace('[-]',color + '[+]' + bcolors.ENDC)
		else:
			print str

	def do(self,ip, StartAddr, Quantity):
		c = connectToTarget(ip,self.options['RPORT'][0])
		if(c == None):
			self.printLine('[-] Modbus is not running on : ' + ip,bcolors.WARNING)
			return None
		self.printLine('[+] Connecting to ' + ip,bcolors.OKGREEN)
		ans = c.sr1(ModbusADU(transId=getTransId(),unitId=int(self.options['UID'][0]))/ModbusPDU01_Read_Coils(startAddr=int(StartAddr,16),quantity=int(Quantity,16)),timeout=timeout, verbose=0)
		ans = ModbusADU_Answer(str(ans))
		self.printLine('[+] Response is :',bcolors.OKGREEN)
		ans.show()
		time.sleep(3)
		

if __name__ == '__main__':
	m = Module()
	m.exploit()
