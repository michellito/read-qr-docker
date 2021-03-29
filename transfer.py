import requests
import argparse

parser = argparse.ArgumentParser(
    description='Transfer ReadsPerGene.out.tab files generated by STAR to DMAC Olympus server.'
)

# parser.add_argument('--file',
#                        type=argparse.FileType('r'),
#                        help='the file to transfer')

parser.add_argument('--path',
                       type=str,
                       help='the destination folder')

parser.add_argument('--rename',
                       type=str,
                       help='descriptive name for file')

parser.add_argument('--url',
                       type=str,
                       help='POST url endpoint')


args = parser.parse_args()
print(args)

data = {
    'rename': args.rename,
    'path': args.path
}

with open("ReadsPerGene.out.tab", "rb") as a_file:
    file_dict = {args.rename: a_file}
    response = requests.post('https://' + args.url, files=file_dict, data=data)
    print(response)