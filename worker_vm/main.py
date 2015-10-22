import time
from server_start import initialize
from server_stop  import terminate

def main():
	name = "instance-lab3-joakim-worker"
	print "Terinating Server"
	terminate(name)
	time.sleep(20)
	print "Starting Server"
	s, floatingIP = initialize(name)
	print s
	print floatingIP

if __name__ == "__main__":
	main()