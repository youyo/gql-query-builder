# coding: utf-8


from typing import Dict, List, Union


class GqlQuery():
    def __init__(self) -> None:
        self.object: str = ''
        self.return_field: str = ''
        self.query_field: str = ''
        self.operation_field: str = ''
        self.fragment_field: str = ''

    def remove_duplicate_spaces(self, query: str) -> str:
        return " ".join(query.split())

    def fields(self, fields: List, name: str = '', condition_expression: str = ''):
        query = '{ ' + " ".join(fields) + ' }'
        if name != '':
            if condition_expression != '':
                query = f'{name} {condition_expression} {query}'
            else:
                query = f'{name} {query}'
        self.return_field = query
        return self

    def query(self, name: str, alias: str = '', input: Dict[str, Union[str, int]] = {}):
        self.query_field = name
        inputs: List[str] = []
        if input != {}:
            for key, value in input.items():
                inputs.append(f'{key}: {value}')
            self.query_field = self.query_field + '(' + ", ".join(inputs) + ')'
        if alias != '':
            self.query_field = f'{alias}: {self.query_field}'

        return self

    def operation(self, query_type: str = 'query', name: str = '', input: Dict[str, Union[str, int]] = {}, queries: List[str] = []):
        self.operation_field = query_type
        inputs: List[str] = []
        if name != '':
            self.operation_field = f'{self.operation_field} {name}'
            if input != {}:
                for key, value in input.items():
                    inputs.append(f'{key}: {value}')
                self.operation_field = self.operation_field + '(' + ", ".join(inputs) + ')'

        if queries != []:
            self.object = self.operation_field + ' { ' + " ".join(queries) + ' }'

        return self

    def fragment(self, name: str, interface: str):
        self.fragment_field = f'fragment {name} on {interface}'
        return self

    def generate(self) -> str:
        if self.fragment_field != '':
            self.object = f'{self.fragment_field} {self.return_field}'
        else:
            if self.object == '' and self.operation_field == '' and self.query_field == '':
                self.object = self.return_field
            elif self.object == '' and self.operation_field == '':
                self.object = self.query_field + ' ' + self.return_field
            elif self.object == '':
                self.object = self.operation_field + ' { ' + self.query_field + ' ' + self.return_field + ' }'

        return self.remove_duplicate_spaces(self.object)
