Script em Python para conexão com Banco de Dados Postgresql, através de tunel SSH.

Paramiko é usado para executar comandos remotos SSH ou transferir arquivo via ftp.

SSHTunnel é usado para acessar bancos de dados e fazer o port Forwarding.
Ele usa o paramiko internamente.
Normalmente o banco não permite a conexão direta, porque a porta é protegida, então ele precisa de um acesso via conexão local (localhost).
