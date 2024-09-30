# Anything in current terminal will be built to minikube docker reg
eval $(minikube docker-env)


# 1

# build then
minikube image load deposit-job

# OR
# 2
minikube image build -t deposit-job -f Dockerfile.jobs .