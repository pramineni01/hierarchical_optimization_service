import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create an optimization problem in a JSON format.')
    parser.add_argument('--type', '-t',
        default= 'year',
        choices=['day', 'month', 'year'],
        required=False,
        help='Problem type: year, month, day.')
    parser.add_argument('--start', '-s',
        default= '2021-01-01 00:00:00',
        required=False,
        help='Start date for the optimization problem.')
    parser.add_argument('--end', '-e',
        default= '2021-12-31 23:45:00',
        required=False,
        help='Start date for the optimization problem.')
    parser.add_argument('--res', '-r',
        default= '960',
        required=False,
        help='Time step in seconds.')
    parser.add_argument('--path', '-p',
        default= './assetsim_interface_client/input-json.json',
        required=False,
        help='Full path to the output file.')
    args = vars(parser.parse_args())
