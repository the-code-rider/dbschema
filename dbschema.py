import argparse

from sqllite_schema import SQLLiteToSchema

if __name__ == '__main__':
    # Create the parser

    # todo: add output format, output file name,

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--dbfile', dest='dbfile', action='store_const', required=True,
                        help='sum the integers (default: find the max)')

    # Parse the arguments
    args = parser.parse_args()

    # only sqlite for now
    # todo : add support for more database

    sqlite = SQLLiteToSchema(args.dbfile)
    schema = sqlite.get_schema()

