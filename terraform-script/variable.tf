variable "region" {
  description = "region of our application"
  type = string
  default = "us-east-1"
}

variable "cluster_name" {
  description = "name of the cluster"
  type = string
  default = "slack-bot-cluster"
}
