# Definindo a variável da região AWS, que é "us-east-1" por padrão
variable "aws_region" {
  default = "us-east-1"
}

# Definindo a variável para o nome do repositório ECR
variable "ecr_repository" {
  description = "Nome do repositório ECR"
  type        = string
  default     = "ledschallenge"
}

# Definindo a variável para o ID da conta AWS
variable "aws_account_id" {
  description = "ID da conta AWS"
  type        = string
  default     = "445567081351"
}
