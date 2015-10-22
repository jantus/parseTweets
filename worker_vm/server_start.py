import sys, os, time
from novaclient.client import Client


config = {'username':"joan4369", 
          'api_key':"openstack",
          'project_id':"ACC-Course",
          'auth_url':'http://smog.uppmax.uu.se:5000/v2.0',
           }
nc = Client('2',**config)
KEYPAIRNAME = "openstack-joakim"
SERVERNAME = "instance-lab3-joakim-worker"
FLAVOR =  nc.flavors.find(name="m1.medium")
IMAGE = nc.images.find(name="lab3-joakim-worker")
floating_ip = 0

def initialize(name):
    SERVERNAME = name 

    serverList = nc.servers.list(search_opts={'name': SERVERNAME})

    if serverList:
        server = serverList[0]
        print "Found server named:", SERVERNAME
    else:

        try:
            keypair = nc.keypairs.find(name=KEYPAIRNAME)
        except:
            print "Erik was right"

        
        f = open("userdata.yml", "r")
        userdata = f.read()
        server = nc.servers.create(SERVERNAME, IMAGE, FLAVOR, key_name=keypair.name, userdata=userdata)
        print userdata
        f.close()
        
        print "Created server named:", SERVERNAME

    time.sleep(15)
   
    floating_ip = nc.floating_ips.create(nc.floating_ip_pools.find(name="ext-net").name)
    try:
        server.add_floating_ip(floating_ip)
        print "Associated ip "+str(floating_ip.ip)+" with instance"
    except:
        print "Could not associate ip with instance, terminated with message:",sys.exc_info()[0]
        print "Current IPs associated with instance", nc.servers.ips(server)



    return server, floating_ip.ip

def terminate(): 
    # Terminate all your running instances
    serverList = nc.servers.list(search_opts={'name': SERVERNAME})
    if serverList:
        server = serverList[0]
        print "Found server named:", SERVERNAME
    try:
        nc.servers.delete(server)
        print "Server terminated"
        sleep(15)
    except:
        print "Server is not definded"


