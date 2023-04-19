variable "stack_name" {
  default = "davila-sample"
}

# Create a VPC

resource "aws_vpc" "this" {
  cidr_block = "10.10.0.0/16"

  tags = {
    Name = "${var.stack_name}-vpc"
  }
}

# Create two Subnets: Public and Private

resource "aws_subnet" "this_public" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.10.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "${var.stack_name}-public-subnet"
  }
}

resource "aws_subnet" "this_private" {
  vpc_id            = aws_vpc.this.id
  cidr_block        = "10.10.2.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "${var.stack_name}-private-subnet"
  }
}

# Create Internet Gateway

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "${var.stack_name}-igw",
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

#   ingress {
#     from_port   = 80
#     to_port     = 80
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["190.60.234.237/32"]
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

  # user_data = <<-EOF
  # #!/bin/bash -ex

  # amazon-linux-extras install nginx1 -y
  # echo "<h1>$(curl https://api.kanye.rest/?format=text)</h1>" >  /usr/share/nginx/html/index.html 
  # systemctl enable nginx
  # systemctl start nginx
  # EOF

  tags = {
    "Name" : "${var.stack_name}",
    "eks:testing" = "yes"
  }
}