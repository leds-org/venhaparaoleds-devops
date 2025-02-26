# Configuração do provedor AWS, definindo a região onde os recursos serão criados
provider "aws" {
  region = var.aws_region
}

# Criando uma instância EC2 para hospedar o servidor da API
resource "aws_instance" "ledschallenge_api_server" {
  ami           = "ami-02a53b0d62d37a757"  # AMI Amazon Linux 2 AMI (HVM) - Kernel 5.10, SSD Volume Type
  instance_type = "t3.micro"  # Tipo da instância (t3.micro é uma opção mais barata)
  key_name      = "terrafomr_create_ec2"  # Nome da chave SSH para acesso
  security_groups = [aws_security_group.ledschallenge_api_sg.name]  # Associando o grupo de segurança
  iam_instance_profile = aws_iam_instance_profile.ledschallenge_ec2_role.name  # Associando o perfil IAM

  user_data = <<-EOF
              #!/bin/bash
              # Atualizando pacotes do sistema
              sudo yum update -y  

              # Instalando o Docker
              sudo amazon-linux-extras enable docker
              sudo yum install -y docker
              
              # Iniciando e ativando o Docker
              sudo systemctl start docker
              sudo systemctl enable docker
              
              # Adicionando o usuário ec2-user ao grupo docker
              sudo usermod -aG docker ec2-user
              
              # Instalando AWS CLI v2
              sudo yum install -y aws-cli
              
              # Baixando e rodando o container do Docker Hub
              sudo docker pull shubert2/ledschallenge:latest  # Substitua pelo seu repositório no Docker Hub
              sudo docker run -d -p 8000:8000 --name ledschallenge-api shubert2/ledschallenge:latest
              EOF

  tags = {
    Name = "LedschallengeAPIInstance"  # Definindo uma tag para identificar a instância
  }
}

# Criando o grupo de segurança para a API, permitindo acesso HTTP e SSH
resource "aws_security_group" "ledschallenge_api_sg" {
  name        = "ledschallenge_api_security_group"
  description = "Permitir acesso HTTP e SSH"

  # Regra de entrada para permitir tráfego HTTP (porta 8000) de qualquer IP
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Regra de entrada para permitir tráfego SSH (porta 22) de qualquer IP
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Regra de saída permitindo tráfego para qualquer destino
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Criando um papel IAM para a instância EC2
resource "aws_iam_role" "ledschallenge_ec2_role" {
  name = "ledschallenge_ec2_role"

  assume_role_policy = <<EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
  EOF
}

# Criando o perfil IAM que será atribuído à instância EC2
resource "aws_iam_instance_profile" "ledschallenge_ec2_role" {
  name = "ledschallenge_ec2_instance_profile"
  role = aws_iam_role.ledschallenge_ec2_role.name
}
