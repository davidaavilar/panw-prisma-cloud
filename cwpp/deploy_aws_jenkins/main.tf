variable "stack_name" {
  default = "davila-jenkins"
}

# Create a VPC

resource "aws_vpc" "this" {
  cidr_block = "10.20.0.0/16"

  tags = {
    Name = "${var.stack_name}-vpc"
  }
}

# Create two Subnets: Public and Private

resource "aws_subnet" "this_public" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.20.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "${var.stack_name}-public-subnet"
  }
}

resource "aws_subnet" "this_private" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.20.2.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "${var.stack_name}-private-subnet"
  }
}

# Create Internet Gateway

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "${var.stack_name}-igw"
  }
}

# Create Public Route Table (to Internet Gateway)

resource "aws_route_table" "this_public" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }

  route {
    ipv6_cidr_block = "::/0"
    gateway_id      = aws_internet_gateway.this.id
  }

  tags = {
    Name = "${var.stack_name}-public-route-table"
  }
}

resource "aws_route_table_association" "this_public" {
  subnet_id      = aws_subnet.this_public.id
  route_table_id = aws_route_table.this_public.id
}

# Create security groups to allow specific traffic

resource "aws_security_group" "web_sg" {
  name   = "${var.stack_name}-sg"
  vpc_id = aws_vpc.this.id

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["34.100.27.241/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web_instance" {
  ami           = "ami-002070d43b0a4f171" # Amazon Linux "ami-0533f2ba8a1995cf9"
  instance_type = "t3.small"
  key_name      = "ec2-default"

  subnet_id                   = aws_subnet.this_public.id
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  associate_public_ip_address = true

  user_data = <<-EOF
  #!/bin/bash
  sudo yum update -y
  sudo yum install wget -y
  sudo yum install git -y
  sudo yum install -y yum-utils
  sudo yum install java-11-openjdk.x86_64 -y
  sudo yum install epel-release -y
  sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
  sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  curl --silent --location http://pkg.jenkins-ci.org/redhat-stable/jenkins.repo | sudo tee /etc/yum.repos.d/jenkins.repo
  sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
  sudo yum install jenkins -y
  sudo service jenkins start
  sudo systemctl enable jenkins
  sudo systemctl start docker
  sudo groupadd docker
  sudo usermod -aG docker $USER
  newgrp docker
  sudo usermod -aG docker 'jenkins'
  sudo chmod 777 /var/run/docker.sock
  EOF

  ## Unlock Jenkins
  ## sudo cat /var/lib/jenkins/secrets/initialAdminPassword

  tags = {
    "Name" : "${var.stack_name}"
  }
}