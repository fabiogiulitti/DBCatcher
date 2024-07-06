from ast import List
from core.treepath import TreePath,make_session_id, references
from json import dumps
from widgets.ContentData import ContentData
from core.driver.abstractdriver import AbstractTreeAction
from psycopg2 import connect, extensions

class PSTreeActions(AbstractTreeAction):
    
    def __init__(self) -> None:
        super().__init__()
        methods = [self.__getattribute__(n) for n in self.__dir__() if hasattr(getattr(self, n), 'action_type')]
        for method in methods:
            self._itemActions[getattr(method, 'node_type_in')] = {getattr(method, 'action_type') : method}
        methods = [self.__getattribute__(n) for n in self.__dir__() if hasattr(getattr(self, n), 'node_type_out')]
        for method in methods:
            self._navActions[getattr(method, 'node_type_in')] = method
        

    @TreePath(node_type_in='connections', node_type_out='databases')
    def retrieveDatabases(self, ctx: dict):

        try:
            
            conn = connect(ctx['connectionURI'])
            #references[id] = {'client' : conn}
            cursor = conn.cursor()

            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")

            databases = cursor.fetchall()
            result = []
            for db in databases:
                print(db)
                result.append(db[0])

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Errore durante la connessione a PostgreSQL: {e}")

        return (result,id)

    @TreePath(node_type_in='databases', node_type_out='schemas')
    def retrieveSchemas(self, ctx: dict):
        id = make_session_id()

        dsn = extensions.make_dsn(ctx['connectionURI'], dbname = 'testdb')
        conn = connect(dsn)
        #(ctx['connectionURI'], *dbname = 'testdb')

        cur = conn.cursor()
        cur.execute("""
            SELECT schema_name
            FROM information_schema.schemata
        """)

        schemas = cur.fetchall()
        result = map(lambda n: n[0], schemas)
        return (result, id)

    #@TreePath(node_type_in='databases', node_type_out='collections_holder')
    #def retrieveCollectionsHolding(self, ctx: dict):
#        return (['collections'],ctx['sessionID'])


 #   @TreePath(node_type_in='collections_holder', node_type_out='collections')
#    def retrieveCollections(self, ctx: dict):
#        id = ctx['sessionID']
#        client = references[id]['client']
#        dbName = ctx['path'][0]
#        db = client[ctx['path'][0]]
#        references[id][dbName] = db
#        collections = db.list_collection_names()
#        return (collections,id)
        

#    @ItemAction(node_type_in='collections', action_type = ActionTypeEnum.CLICK)
#    def retrieveFirstDocuments(self, ctx: dict):
#        return getDocuments(ctx)


