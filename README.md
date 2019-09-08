# gql-query-builder

This is a GraphQL query builder.

## Install

```
pip install gql-query-builder
```

## Usage

```
from gql.query.builder import GqlQuery

"""
query { hero { name } }
"""
query = GqlQuery().fields(['name']).query('hero').operation().generate()
print(query)
```
