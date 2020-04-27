import sys
import os
import subprocess
import csv
import glob
import argparse



def main():
    args = parseArgs(sys.argv)

    liftover_binary_installed = checkForLiftOver()
    if not liftover_binary_installed:
        die(
        """Ensure that the liftOver application is in this folder and executable."""
        )

    exists, file_not_found = checkFilesExist(args)
    if not exists:
        die(file_not_found)

    liftCNVfile(args.chain, args.variants, args.pos_col, args.output)



def liftCNVfile(chain_file_path, variants_file_path, pos_col, output_file):
    vf = open(variants_file_path, 'r')
    output_file2 = open(variants_file_path + '.conversions.txt', 'w')
    with vf, output_file:
        reader = csv.reader(vf, delimiter='\t')
        writer1 = csv.writer(output_file, delimiter='\t')
        writer2 = csv.writer(output_file2, delimiter='\t')
        for row in reader:
            if "Position" in row[int(pos_col)-1]:
                continue

            position = row[int(pos_col)-1]
            lifted_position, match_ratio = liftPosition(chain_file_path, position)
            row[int(pos_col)-1] = lifted_position

            if lifted_position is not None:
                writer1.writerow(row)
                writer2.writerow([position, lifted_position, match_ratio])




def liftPosition (chain_file, position):
    # take the position and write it to a temp file
    temp_input_file_path = '_position.temp'
    temp_lifted_file_path = '_liftOver.temp'
    temp_unmap_file_path = "_liftOver.temp.unmap"

    temp_input_file = open(temp_input_file_path, 'w')
    with temp_input_file as f:
        f.write(position)

    lifted_position = ''
    minMatch = 101

    while lifted_position is '':
        minMatch -= 1
        # process the temp file with liftover
        minMatch_str = str(minMatch / 100)
        success = subprocess.call([
            "./liftOver",
            "-positions",
            "-minMatch=" + minMatch_str,
            temp_input_file_path,
            chain_file,
            temp_lifted_file_path,
            temp_unmap_file_path
        ])

        if success == 0:
            # read liftOver's output file and return the position
            lifted_file = open(temp_lifted_file_path, 'r')
            with lifted_file:
                lifted_position = lifted_file.read().rstrip()

            # delete the input temp file and remove all files left by liftOver

            liftOver_temp_files = glob.glob('liftOver_*')
            deleteFiles(liftOver_temp_files)

            if lifted_position is not '' or minMatch is 0:
                deleteFiles([temp_input_file_path, temp_lifted_file_path, temp_unmap_file_path])
                return lifted_position, minMatch_str

        else:
            raise Exception("liftOver app returned a non-zero exit code")



# def convertLiftedBedToCNV(lifted_bed_file_path, header, args):
#     lifted_file = open(lifted_bed_file_path, mode='r')
#     writer = csv.writer(args.output, delimiter='\t' )
#
#     header[0] += '_old'
#     header = ["Position_new"] + header
#     writer.writerow(header)
#
#     with lifted_file, args.output:
#         reader = csv.reader(lifted_file, delimiter='\t')
#         for row in reader:
#             pos = "{}:{}-{}".format(row[0], row[1], row[2])
#             writer.writerow([pos] + row[3:])
#
#     os.remove(lifted_bed_file_path)
#
#     if args.output == sys.stdout:
#         os.rename(lifted_file.name + ".unmap", args.variants + ".unmap")
#     else:
#         os.rename(lifted_file.name + ".unmap", args.output.name + ".unmap")



def checkForLiftOver():
    bash_cmd = './liftOver'
    proc = subprocess.Popen(bash_cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
    )
    stderr = proc.communicate()[1]
    is_installed = "liftOver - Move annotations from one assembly to another" in stderr.decode('utf-8')
    return is_installed


def checkFilesExist(args):
    if not os.path.isfile(args.chain):
        return False, 'Chain file not found: ' + args.chain
    if not os.path.isfile(args.variants):
        return False, 'Variants file not found: ' + args.variants

    return True, None



def parseArgs(args):
    parser = argparse.ArgumentParser(
        description='Lift over PennCNV formatted CNV files')
    parser.add_argument('chain', metavar='ChainFile',
                        help='UCSC Chain File.  Check README for download links.' )
    parser.add_argument('variants', metavar='VariantsFile',
                        help='File containing variants in PennCNV format.')
    parser.add_argument('pos_col', metavar='PositionColumnInVariantsFile', default=1,
                        help='Column with Position within File containing variants in PennCNV format.')
    parser.add_argument('output', metavar='OutputFile', nargs='?', default=sys.stdout,
                        type=argparse.FileType('w'),
                        help='File containing variants in PennCNV format.')

    return parser.parse_args()


def deleteFiles(files):
    for f in files:
        os.remove(f)



def die(error_msg):
    sys.stderr.write(error_msg)
    sys.exit(1)


if __name__ == "__main__":
    main()
