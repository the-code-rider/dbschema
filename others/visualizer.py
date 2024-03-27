import json
from pyvis.network import Network

class Visualizer:

    def __init__(self, heading, directed, background, layout):
        self.net = Network(
            heading=heading,
            directed=directed,
            bgcolor=background
        )

        self.layout = layout

    def _read_file(self, file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
        return data

    def generate_network(self, file_name):
        data = self._read_file(file_name)
        # Dictionary to keep track of tables and their nodes
        table_nodes = {}

        # Add nodes for tables # todo: determine shape and color of nodes, font formatting
        for table in data['tables']:
            table_name = table['name']
            table_nodes[table_name] = table_name
            columns_html = "<br>".join([f"{col['name']} ({col['type']})" for col in table['columns']])
            # title = f"<strong>Table: {table_name}</strong><br>Columns:<br>{columns_html}"
            net.add_node(table_name, label=table_name, title=columns_html, color="white", shape='box')

        # Add edges for foreign keys
        for table in data['tables']:
            if 'foreign_keys' in table:
                for fk in table['foreign_keys']:
                    from_table = table['name']
                    to_table = fk['table']
                    # print(from_table)
                    # print(to_table)
                    if from_table in table_nodes and to_table in table_nodes:
                        net.add_edge(table_nodes[from_table], table_nodes[to_table], title=f"FK to {to_table}")
                    else:
                        print(f"missing entry for : {from_table}, and/or {to_table}")

        # todo: add index

    def generate_html(self, file_name, local=True):
        self.net.generate_html(file_name)



# Load JSON data from file
with open('samples/chroma_db.json', 'r') as file:
    data = json.load(file)

# Create a network graph
net = Network(
    heading='CHROMA DB',
    directed=True,
    bgcolor='gray',
    layout=True
)

# Dictionary to keep track of tables and their nodes
table_nodes = {}

# Add nodes for tables
for table in data['tables']:
    table_name = table['name']
    table_nodes[table_name] = table_name
    columns_html = "<\n>".join([f"{col['name']} ({col['type']})" for col in table['columns']])
    title = f"<strong>Table: {table_name}</strong><br>Columns:<br>{columns_html}"


    net.add_node(table_name, label=title, title=columns_html, color="white", shape='box')

# Add edges for foreign keys
for table in data['tables']:
    if 'foreign_keys' in table:
        for fk in table['foreign_keys']:
            from_table = table['name']
            to_table = fk['table']
            # print(from_table)
            # print(to_table)
            if from_table in table_nodes and to_table in table_nodes:
                net.add_edge(table_nodes[from_table], table_nodes[to_table], title=f"FK to {to_table}")
            else:
                print(f"missing entry for : {from_table}, and/or {to_table}")



net.toggle_physics(True)
# net.show_buttons()
# net.

# Generate and display the network graph
net.show("chroma_db_network.html", notebook=False)
