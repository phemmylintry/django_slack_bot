


#------------------------------------------------------------------------------
# VPC
#------------------------------------------------------------------------------ 

module "vpc" {
    source              = "terraform-aws-modules/vpc/aws"
    
    name                = "slack-bot-vpc"
    cidr                = "10.0.0.0/16"

    azs                 = data.aws_availability_zones.azs.names
    private_subnets     = ["10.0.1.0/24", "10.0.2.0/24"]
    public_subnets      = ["10.0.3.0/24", "10.0.4.0/24"]

    enable_nat_gateway  = true
    single_nat_gateway  = true
    enable_dns_hostnames= true

    public_subnet_tags = {
        "kubernetes.io/cluster/${var.cluster_name}" = "shared"
        "kubernetes.io/role/elb"                    = "1"
    }

    private_subnet_tags = {
        "kubernetes.io/cluster/${var.cluster_name}" = "shared"
        "kubernetes.io/role/elb"                    = "1"
    }
}

resource "aws_security_group" "all_worker_group" {
  name_prefix           = "all_worker_mgt"
  vpc_id                = module.vpc.vpc_id

  ingress {
      from_port         = 80
      to_port           = 80
      protocol          = "tcp"

      cidr_blocks       = ["10.0.0.0/8"]
  }
}


#------------------------------------------------------------------------------
#   CLUSTER
#------------------------------------------------------------------------------


module "eks" {
    source = "terraform-aws-modules/eks/aws"
    version = "~> 18.0"
    cluster_name    = var.cluster_name
    cluster_version = "1.21"

    subnet_ids         = module.vpc.private_subnets
    cluster_endpoint_private_access = true
    vpc_id = module.vpc.vpc_id

    eks_managed_node_groups = {
        green = {
        min_size     = 1
        max_size     = 2
        desired_size = 1

        name           = "slack-bot-node-group"
        instance_types = ["t2.medium"]
        vpc_security_group_ids = [aws_security_group.all_worker_group.id]
        }
    }
}
