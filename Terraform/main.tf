resource "aws_security_group" "weather_db_sg" {
  name        = "weather-db-sg"
  description = "Security group for weather RDS instance"

  tags = {
    Name = "weather-db-sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_postgres_my_ip" {
  security_group_id = aws_security_group.weather_db_sg.id
  description        = "Postgres from my IP"
  cidr_ipv4          = var.my_ip
  from_port          = 5432
  to_port            = 5432
  ip_protocol        = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "allow_all_outbound" {
  security_group_id = aws_security_group.weather_db_sg.id
  description        = "Allow all outbound traffic"
  cidr_ipv4          = "0.0.0.0/0"
  ip_protocol        = "-1"
}

resource "aws_db_instance" "weather_db" {
  identifier             = "weather-db"
  engine                 = "postgres"
  engine_version         = "16"
  instance_class         = "db.t3.micro"
  allocated_storage      = 10
  db_name                = "weather_db"
  username               = var.db_username
  password               = var.db_password
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.weather_db_sg.id]
  skip_final_snapshot    = true
}
