from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
 
db = GraphDatabase("http://localhost:7474", username="neo4j", password="password")
 
#Obtendo todos os usuário que Bob segue na rede
q = 'MATCH (u1:Usuario)-[r:follows]->(u2:Usuario) WHERE u1.name="Bob" RETURN u1, type(r), u2'

results = db.query(q, returns=(client.Node, str, client.Node))

BobSegue = []
for r in results:
    BobSegue.append(r[2]["name"]) 
    print("(%s)-[%s]->(%s)" % (r[0]["name"], r[1], r[2]["name"]))
# saída:
# (Bob)-[follows]->(Alice)

for i in BobSegue:
    print (i)

#obtendo o primeiro usuário que bob segue (poderia ser todos, ou um escolhido aleatoriamente)
primeiro = BobSegue[0]
print (primeiro)

#Obtendo todos os usuário que o "primeiro" segue na rede
q = 'MATCH (u1:Usuario)-[r:follows]->(u2:Usuario) WHERE u1.name="' + primeiro + '" RETURN u1, type(r), u2'
results = db.query(q, returns=(client.Node, str, client.Node))


#Obtendo o nodo de Bob
q = 'MATCH (u1:Usuario) where u1.name="Bob" return u1'
Bob = db.query(q, returns=(client.Node))
#obtendo o únio nodo (segundo [0]) de uma consulta de apenas um único resultado (primeiro [0])
u1 = Bob[0][0]

for r in results:    
    u2 = db.nodes.create(name=r[2]["name"])
    print("(%s)-[%s]->(%s)" % (r[0]["name"], r[1], r[2]["name"]))
    print("Bob, talvez você pode querer seguir " + r[2]["name"])
    resp =  input("Seguir (s | n): ")
    if resp == "s":
        u1.relationships.create("follows", r[2])
