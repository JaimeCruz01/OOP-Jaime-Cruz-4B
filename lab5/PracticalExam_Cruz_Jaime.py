servers_list = []

class servers():
    def __init__(self, hostname, ipaddress, ram_capacity, status):
        self.hostname = hostname
        self.ipaddress = ipaddress
        self.ram_capacity = ram_capacity
        self.status = status

    def turnoff(self):
         if self.status == "off":
              print("The server is alredy off")
         else:
              self.status = "off"

    def turnon(self):
             if self.status == "on":
                  print("The server is alredy on")
             else:
                  self.status = "on"  

    def updateRam(self, newram):
         self.ram_capacity = newram

class datacenter():
    def __init__(self, region, servers):
            self.region = region
            self.servers = servers

    def addserver(self, server):
        self.servers.append(server)

    def showactiveservers(self):
        active = 0
        for i in self.servers:
            if i.status == "on":
                print(f"Servidor: {i.hostname}")
                active += 1
        if active == 0:
             print("There wasnt servers available")

server1 = servers("servidor1", "189.126.0.0.1", "16", "off")
server2 = servers("servidor2", "189.126.0.0.1", "16", "on")
data1 = datacenter("Mexico", servers_list)
data1.addserver(server1)
data1.addserver(server2)
#data1.showactiveservers()
#server1.turnoff()
#data1.showactiveservers()
#server1.turnon()
data1.showactiveservers()

