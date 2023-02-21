import requests, argparse

parser = argparse.ArgumentParser()

parser.add_argument("-o", "--Output", help = "Show Output")

args = parser.parse_args()

if args.Output:
    print("Displaying Output as: % s" % args.Output)