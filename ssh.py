from sshtunnel import SSHTunnelForwarder
import psycopg2

# ====== Configurações SSH ======
ssh_host = '192.168.1.190'  #IP ou url de conexão
ssh_port = 22
ssh_user = 'seu_usuario'
ssh_password = 'sua_senha'

# ====== Configurações PostgreSQL ======
db_host = '127.0.0.1'  # Sempre localhost ao usar o túnel
db_port = 5432         # Porta padrão PostgreSQL
db_name = 'seu_banco'
db_user = 'seu_usuario_db'
db_password = 'sua_senha_db'

# Porta local livre para bind
local_bind_port = 6543

# ====== Cria túnel SSH ======
with SSHTunnelForwarder(
    (ssh_host, ssh_port),
    ssh_username=ssh_user,
    ssh_password=ssh_password,
    remote_bind_address=('127.0.0.1', db_port),
    local_bind_address=('127.0.0.1', local_bind_port)
) as tunnel:

    print(f"Túnel SSH estabelecido: localhost:{local_bind_port} → {ssh_host}:{db_port}")

    # ====== Conexão PostgreSQL via túnel ======
    try:
        print("Conectando ao banco de dados PostgreSQL via túnel SSH...")

        conn = psycopg2.connect(
            host=db_host,
            port=tunnel.local_bind_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        cursor = conn.cursor()
        print("Conexão PostgreSQL estabelecida.")

        # Executa a query
        query = 'SELECT * FROM project;'
        cursor.execute(query)

        # Obtém os resultados
        rows = cursor.fetchall()
        print("Resultados da consulta:")
        for row in rows:
            print(row)

    except psycopg2.Error as e:
        print(f"Erro ao conectar ou executar a query no PostgreSQL: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        print("Conexão PostgreSQL encerrada.")

print("Túnel SSH encerrado.")
