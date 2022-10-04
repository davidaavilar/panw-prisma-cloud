# variables.tf

variable "aws_region" {
  description = "The AWS region things are created in"
  default     = "us-east-1"
}

variable "app_prefix" {
  default = "my-sample-app"
}

variable "ecs_task_execution_role_name" {
  description = "ECS task execution role name"
  default     = "myEcsTaskExecutionRole"
}

variable "az_count" {
  description = "Number of AZs to cover in a given region"
  default     = "2"
}

variable "app_image" {
  description = "Docker image to run in the ECS cluster"
  default     = "nginx:latest"
}

variable "app_port" {
  description = "Port exposed by the docker image to redirect traffic to"
  default     = 80
}

variable "app_count" {
  description = "Number of docker containers to run"
  default     = 2
}

variable "command" {
  description = "The Docker CMD that is passed to the container."
  default     = ["nginx", "-g", "daemon off;"]
}

variable "entrypoint" {
  description = "The Docker ENTRYPOINT that is passed to the container."
  default     = ["/docker-entrypoint.sh"]
}

variable "health_check_path" {
  default = "/"
}

variable "fargate_cpu" {
  description = "Fargate instance CPU units to provision (1 vCPU = 1024 CPU units)"
  default     = 1024
}

variable "fargate_memory" {
  description = "Fargate instance memory to provision (in MiB)"
  default     = 2048
}