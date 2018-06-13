import argparse
import json
import myouji_kenchi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_json')
    parser.add_argument('output_path')
    args = parser.parse_args()

    frequency_data = json.load(open(args.input_json))
    strings, weights = zip(*frequency_data.items())
    acceptor = myouji_kenchi.transducer.acceptor_for_strings(strings, weights)
    #acceptor.write(args.output_path)
    open(args.output_path, mode='wb').write(acceptor.__str__())


if __name__ == '__main__':
    main()
