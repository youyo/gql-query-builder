# gql-query-builder

![](https://github.com/youyo/gql-query-builder/workflows/Publish%20python%20package/badge.svg)

This is a GraphQL query builder.  
Use with method chain.

## Install

```
pip install gql-query-builder
```

## Usage

- query

```python
from gql_query_builder import GqlQuery

query = GqlQuery().fields(['name']).query('hero').operation().generate()
print(query)
"""
query {
    hero {
        name
    }
}
"""
```

- mutation

```python
from gql_query_builder import GqlQuery

query = GqlQuery().fields(['stars', 'commentary']).query('createReview', input={"episode": "$ep", "review": "$review"}).operation('mutation', name='CreateReviewForEpisode', input={"$ep": "Episode!", "$review": "ReviewInput!"}).generate()
print(query)
"""
mutation CreateReviewForEpisode($ep: Episode!, $review: ReviewInput!) {
    createReview(episode: $ep, review: $review) {
        stars
        commentary
    }
}
"""
```

### Methods

- `fields()`  
  build response fields.

```python
#Syntax

fields(
    fields: List[str] = [],
    name: str = '',
    condition_expression: str = ''
)
```

- `query()`  
  build query fields.

```python
#Syntax

query(
    name: str = '',
    alias: str = '',
    input: Dict[str, Union[str, int]] = {}
)
```

- `operation()`  
  build operation fields.

```python
#Syntax

operation(
    query_type: str = 'query',
    name: str = '',
    input: Dict[str, Union[str, int]] = {},
    queries: List[str] = []
)
```

- `fragment()`  
  build fragment fields.

```python
#Syntax

fragment(
    name: str,
    interface: str
)
```

- `generate()`  
  generate query.

```python
#Syntax

generate()
```

## Examples

- Nesting fields

```python
from gql_query_builder import GqlQuery

field_friends = GqlQuery().fields(['name'], name='friends').generate()
query = GqlQuery().fields(['name', field_friends]).query('hero').operation('query').generate()
print(query)
"""
query {
    hero {
        name
        friends {
            name
        }
    }
}
"""
```

- Query with input

```python
from gql_query_builder import GqlQuery

query = GqlQuery().fields(['name', 'height']).query('human', input={"id": '"1000"'}).operation().generate()
print(query)
"""
query {
    human(id: "1000") {
        name
        height
    }
}
"""
```

- Query with nested input

```python
from gql_query_builder import GqlQuery
GqlQuery().fields(['name', 'height']).query('human', input={"input": {"data": {"id": "1000", "name": "test"}}}).operation().generate()
"""
query{
    human(input: {data: {id: "1000", name: "test"}}){
        human{
            name, 
            height
        }
    }
}
"""
```

- Query with input and arguments

```python
from gql_query_builder import GqlQuery

query = GqlQuery().fields(['name', 'height(unit: FOOT)']).query('human', input={"id": '"1000"'}).operation().generate()
print(query)
"""
query {
    human(id: "1000") {
        name
        height(unit: FOOT)
    }
}
"""
```

- Alias

```python
from gql_query_builder import GqlQuery

query_empirehero = GqlQuery().fields(['name']).query('hero', alias='empireHero', input={"episode": 'EMPIRE'}).generate()
query_jedihero = GqlQuery().fields(['name']).query('hero', alias='jediHero', input={"episode": 'JEDI'}).generate()
query = GqlQuery().operation('query', queries=[query_empirehero, query_jedihero]).generate()
print(query)
"""
query {
    empireHero: hero(episode: EMPIRE) {
        name
    }
    jediHero: hero(episode: JEDI) {
        name
    }
}
"""
```

- Fragments

```python
from gql_query_builder import GqlQuery

field_friends = GqlQuery().fields(['name'], name='friends').generate()
query = GqlQuery().fields(['name', 'appearsIn', field_friends]).fragment('comparisonFields', 'Character').generate()
print(query)
"""
fragment comparisonFields on Character {
    name
    appearsIn
    friends {
        name
    }
}
"""
```

- Refer to fragments

```python
from gql_query_builder import GqlQuery

query_leftComparison = GqlQuery().fields(['...comparisonFields']).query('hero', alias='leftComparison', input={"episode": "EMPIRE"}).generate()
query_rightComparison = GqlQuery().fields(['...comparisonFields']).query('hero', alias='rightComparison', input={"episode": "JEDI"}).generate()
query = GqlQuery().operation('query', queries=[query_leftComparison, query_rightComparison]).generate()
print(query)
"""
query {
    leftComparison: hero(episode: EMPIRE) {
        ...comparisonFields
    }
    rightComparison: hero(episode: JEDI) {
        ...comparisonFields
    }
}
"""
```

- Query with variables

```python
from gql_query_builder import GqlQuery

field_friends = GqlQuery().fields(['name'], name='friends').generate()
query = GqlQuery().fields(['name', field_friends]).query('hero', input={"episode": "$episode"}).operation('query', name='HeroNameAndFriends', input={"$episode": "Episode"}).generate()
print(query)
"""
query HeroNameAndFriends($episode: Episode) {
    hero(episode: $episode) {
        name
        friends {
            name
        }
    }
}
"""
```

- Directives

```python
from gql_query_builder import GqlQuery

field_friends = GqlQuery().fields(['name'], name='friends @include(if: $withFriends)').generate()
query = GqlQuery().fields(['name', field_friends]).query('hero', input={"episode": "$episode"}).operation('query', name='Hero', input={"$episode": "Episode", "$withFriends": "Boolean!"}).generate()
print(query)
"""
query Hero($episode: Episode, $withFriends: Boolean!) {
    hero(episode: $episode) {
        name
        friends @include(if: $withFriends) {
            name
        }
    }
}
"""
```
