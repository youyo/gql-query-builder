# coding: utf-8


from typing import Dict, List, Union


class GqlQueryException(Exception):
    pass


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
        if not fields:
            raise GqlQueryException('fields cannot be empty or null')
        query = '{ ' + " ".join(fields) + ' }'
        if name != '':
            if condition_expression != '':
                query = f'{name} {condition_expression} {query}'
            else:
                query = f'{name} {query}'
        self.return_field = query
        return self

    @staticmethod
    def build_input(input: Dict[str, Union[str, int]], initial_str: str):
        inputs: List[str] = []

        final_str = initial_str

        if input != {}:
            key = list(input.keys())[0]
            nested_keys = list()

            while isinstance(input[key], dict):
                nested_keys.append(key)
                input = input[key]
                key = list(input.keys())[0]

            for key, value in input.items():
                if nested_keys:
                    inputs.append(f'{key}: "{value}"')  # Nested input won't have double quotes

                else:
                    inputs.append(f'{key}: {value}')

            final_str += '('

            for key in nested_keys:
                final_str = final_str + key + ': {'

            final_str = final_str + ", ".join(inputs)

            for _ in nested_keys:
                final_str += '}'

            final_str += ')'

        return final_str

    def query(self, name: str, alias: str = '', input: Dict[str, Union[str, int]] = {}):
        self.query_field = name
        self.query_field = self.build_input(input, self.query_field)
        if alias != '':
            self.query_field = f'{alias}: {self.query_field}'

        return self

    def operation(self, query_type: str = 'query', name: str = '', input: Dict[str, Union[str, int]] = {},
                  queries: List[str] = []):
        self.operation_field = query_type
        if name != '':
            self.operation_field = f'{self.operation_field} {name}'
            self.operation_field = self.build_input(input, self.operation_field)

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
