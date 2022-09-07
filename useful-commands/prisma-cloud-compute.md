
### Useful Commands to speed up deployments...

<H2>Deploy Minikube Cluster on MacOS</H2>

```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube
```

```
minikube start
```

**What you’ll need:**
- 2 CPUs or more
- 2GB of free memory
- 20GB of free disk space
- Internet connection
- Container or virtual machine manager, such as: Docker, Hyperkit, Hyper-V, KVM, Parallels, Podman, VirtualBox, or VMware Fusion/Workstation

Source: https://minikube.sigs.k8s.io/docs/start/

<H2>Deploy EKS Cluster using eksctl</H2>

Installing `eksctl`:

https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html

To create a EKS Cluster:

```
eksctl create cluster --name <YOUR_CLUSTER_NAME> --region <YOUR_REGION> --nodegroup-name <NODE_GROUP_NAME> --node-type t3.xlarge  --nodes 2 --nodes-min 2 --nodes-max 4 --version 1.21 --managed
```

To access to your cluster using kubeconfig:

```
aws eks update-kubeconfig --name=<YOUR_CLUSTER_NAME>
```

Then, try to view your nodes:

```
kubectl get node
```

Deleting your EKS Cluster:

```
eksctl create cluster --name <YOUR_CLUSTER_NAME> --region <YOUR_REGION> 
```


<H2>Deploy AKS Cluster using 'azure cli' </H2>

Installing `azure cli`:

https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

To create a AWS Cluster:

```
export LOCATION=eastus
export RESOURCEGROUP=<YOUR_RG_NAME>
export CLUSTER=<YOUR_CLUSTER_NAME>
```

```
az group create --name $RESOURCEGROUP --location $LOCATION
```

```
az aks get-versions --location $LOCATION
```

```
az aks create --resource-group $RESOURCEGROUP --name $CLUSTER --node-count 2 --enable-addons monitoring --generate-ssh-keys --node-vm-size Standard_D4_v2 --kubernetes-version 1.21.9
```

To access to your cluster using kubeconfig:

```
aws eks update-kubeconfig --name=<YOUR_CLUSTER_NAME>
```

Connecting with your AKS Cluster:

```
az aks get-credentials --resource-group $RESOURCEGROUP --name $CLUSTER
```

Then, try to view your nodes:

```
kubectl get node
```

Deleting your AKS Cluster:

```
az group delete --resource-group $RESOURCEGROUP
```





