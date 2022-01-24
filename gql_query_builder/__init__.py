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


def build_input_2(input: Dict[str, Union[str, int]], initial_str: str, nest= 0, other_input = {}):
    if(initial_str==''):
        final_str = '('+initial_str
    else: 
        final_str = initial_str 
    if(not bool(input)):
        if(bool(other_input)):
            final_str = final_str + ','
            return build_input_2(other_input, final_str, nest, {})
        else:
            return final_str + ')'
    key = list(input.keys())[0]
    val = input[key]
    if(not isinstance(val, dict)):
        input.pop(key, {})
        if(bool(input)):
            final_str+=f' {key}: {val},'
        else: 
            if(nest >0):
                final_str+=f' {key}: "{val}" ' + ' }' * nest
            else: 
                final_str+=f' {key}: "{val}"'
        return build_input_2(input,final_str, nest, other_input)
    else:
        nest= nest+1
        final_str+=f' {key}:' + ' {'
        other_input = without_keys(input, key) 
        return build_input_2(val, final_str, nest, other_input)

def without_keys(d, keys):
     return {x: d[x] for x in d if x not in keys}