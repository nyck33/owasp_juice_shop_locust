from graphql import build_ast_schema, parse
from graphql.language.printer import print_ast

def extract_operations(schema_path):
    with open(schema_path) as file:
        schema = file.read()

    ast = parse(schema)
    built_schema = build_ast_schema(ast)

    queries = []
    mutations = []

    for type_name in built_schema.type_map:
        if type_name == 'Query':
            fields = built_schema.type_map[type_name].fields
            queries.extend(fields)
        elif type_name == 'Mutation':
            fields = built_schema.type_map[type_name].fields
            mutations.extend(fields)

    return queries, mutations

def write_to_file(filename, items):
    with open(filename, 'w') as file:
        for item in items:
            file.write(print_ast(item.ast_node) + '\n\n')

def main():
    schema_path = 'storefront_schema.graphql'
    queries, mutations = extract_operations(schema_path)

    write_to_file('queries.py', queries)
    write_to_file('mutations.py', mutations)

if __name__ == "__main__":
    main()
