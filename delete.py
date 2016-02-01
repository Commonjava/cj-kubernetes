import sys
import kubesvc as k

if len(sys.argv) < 2:
	print "Usage: %s <service-name>" % sys.argv[0]
	exit(1)

service=sys.argv[1]
port = k.get_service_port(service)

if not port:
    print "Cannot find exposed port for service: %s" % service
    exit(2)

k.protect_service_port(service, port)
