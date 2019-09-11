# coding: utf-8


from gql_query_builder import GqlQuery
from graphqlclient import GraphQLClient


if __name__ == '__main__':
    # create client
    client = GraphQLClient('https://countries.trevorblades.com/')

    # generate query
    query = GqlQuery()\
        .fields(['name', 'native', 'emoji'])\
        .query('country', input={"code": '"JP"'})\
        .operation('query')\
        .generate()

    # execute
    response = client.execute(query)
    print(response)
