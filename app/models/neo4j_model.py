from py2neo import Graph, DatabaseError
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


# Conexión a Neo4j - Asegúrate de cambiar estos valores
graph = Graph("bolt://localhost:7690", auth=("neo4j", "123456789"))

def get_data():
    # Ejemplo de consulta a Neo4j
    query = "MATCH (n) RETURN n LIMIT 5"
    return graph.run(query).data()

def test_connection():
    try:
        # Ejecuta una consulta simple
        graph.run("MATCH (n) RETURN n LIMIT 1")
        return "Conexión exitosa a Neo4j."
    except DatabaseError as e:
        return f"Error en la conexión a Neo4j: {e}"
    
def verify_credentials(username, password):
    # Obtener el usuario basado en el username
    query = "MATCH (u:Usuario {username: $username}) RETURN u"
    result = graph.run(query, username=username).data()

    if len(result) > 0:
        user = result[0]['u']
        # Comparar el hash de la contraseña almacenada con la contraseña proporcionada
        if check_password_hash(user['password'], password):
            return True

    return False


def create_user(nombre, apellido, username, password, rol):
    hashed_password = generate_password_hash(password)
    user_query = """
    CREATE (u:Usuario {nombre: $nombre, apellido: $apellido, username: $username, password: $hashed_password})
    RETURN u
    """
    user = graph.run(user_query, nombre=nombre, apellido=apellido, username=username, hashed_password=hashed_password).data()

    if rol == 'estudiante':
        relation_query = """
        MATCH (u:Usuario {username: $username})
        CREATE (u)-[:ES]->(e:Estudiante {})
        """
    elif rol == 'educador':
        relation_query = """
        MATCH (u:Usuario {username: $username})
        CREATE (u)-[:ES]->(e:Educador {})
        """
    else:
        return None  # O manejar de otra forma si el rol no es válido

    graph.run(relation_query, username=username)
    return user

def get_user_info(username):
    query = """
    MATCH (u:Usuario {username: $username})
    OPTIONAL MATCH (u)-[:ES]->(e:Estudiante)
    OPTIONAL MATCH (u)-[:ES]->(d:Educador)
    RETURN u, CASE WHEN e IS NOT NULL THEN 'Estudiante' WHEN d IS NOT NULL THEN 'Educador' ELSE 'Desconocido' END as rol
    """
    result = graph.run(query, username=username).data()
    if result:
        user_info = result[0]['u']
        user_info['rol'] = result[0]['rol']
        return user_info
    return None

