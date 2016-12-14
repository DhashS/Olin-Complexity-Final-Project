ipcluster stop 2>&1
sleep 5
ipcluster start --n=$1 --daemonize
sleep 10
echo "Cluster up with $1 engines"
