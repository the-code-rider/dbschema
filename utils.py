import json

def save_to_file(schema, output_filename, pretty_print=True):
    with open(output_filename, 'w') as f:
        if pretty_print:
            f.write(json.dumps(schema, indent=4))
        else:
            f.write(json.dumps(schema))
