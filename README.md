DevOps Final Project INT College full DevOps Circle Development & Kubernetes & CI/CD With Jenkins & Monitoring


Kubernetes Cluster and Infrastructure Setup:

Built a production-quality Kubernetes cluster using EC2 instances with Ubuntu.
Established a cluster with one control plane and multiple worker nodes in different AZs.
Configured essential Kubernetes components like apiserver, etcd, kube-scheduler, kube-controller-manager, and cloud-controller-manager.
Implemented IAM roles, a single security group, and deployed a medium Ubuntu EC2 instance.
Installed container runtime, aligning machine hostname with AWS, and installed kubeadm, kubelet, and kubectl.


Kubernetes Cluster Initialization and Configuration:

Initialized control-plane node using kubeadm init.
Integrated AWS Cloud Controller Manager for Kubernetes-AWS service interactions.
Deployed a CNI addon for pod-to-pod communication.
Joined worker nodes and installed the EBS CSI driver for persistent storage.
Deployed Kubernetes Dashboard with secure token-based access.


Object Detection Service Deployment:

Created a GitHub repository for the project with Kubernetes manifests.
Managed Docker images for polybot and yolo5 microservices.
Configured Kubernetes manifests including probes, resource limits, autoscaling, and graceful termination.


Telegram Integration and Service Monitoring:

Implemented Nginx ingress controller for handling Telegram traffic.
Set up service monitoring tools: Grafana, FluentD, and Prometheus with necessary integrations and dashboards.
CI/CD Pipeline Implementation:

Provisioned separate AWS resources for development and production environments with distinct Telegram tokens.
Utilized Jenkins for CI, organizing pipelines in dev and prod folders.
Developed build pipelines for polybot and yolo5 services, automating triggers upon source code changes.
Tagged new Docker images with unique identifiers for different builds.

Deployment Automation with ArgoCD (GitOps):

Prepared distinct Kubernetes namespaces and YAML manifests for dev and prod environments.
Installed and configured ArgoCD in the Kubernetes cluster.
Created releases-dev and releases-prod Jenkinsfiles for automated deployment post-build.
Configured ArgoCD for automatic deployment in dev and manual in prod environments.
