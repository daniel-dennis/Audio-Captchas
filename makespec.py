import os
import time
import multiprocessing as mp
from subprocess import Popen
import cv2
import argparse

def chunks(l, n):
    try:
        for i in range(0, len(l), n):
            yield l[i:i + n]
    except ValueError:
        yield l

def gen_spectograms(items, input_dir, output_dir):
    for filename in items:
        if filename.endswith('.mp3'):
            popenarg = 'sox %s -n spectrogram -r -x 128 -y 64 -o %s.jpg' % (os.path.join(input_dir, filename), (os.path.join(output_dir, filename[0:8])))
            with Popen(args=popenarg.split()) as proc:
                proc.wait()
            try:
                cv2.imwrite(os.path.join(output_dir, filename[0:8] + '.jpg'),  cv2.resize(cv2.imread(os.path.join(output_dir, filename[0:8]) + '.jpg'), dsize=(128, 64), interpolation=cv2.INTER_CUBIC))
            # In case the .mp3 file was corrupt
            except cv2.error:
                pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', help='The directory for input files', type=str)
    parser.add_argument('--output_dir', help='Where the spectograms are stored', type=str)
    args = parser.parse_args()

    if args.input_dir is None:
        print('Please specify --input_dir to generate')
        exit(1)
    if args.output_dir is None:
        print('Please specify --output_dir to output to')
        exit(1)

    print('Generating spectograms')
    start = time.time()

    procs = []
    dirlist = os.listdir(args.input_dir)

    if len(dirlist) == 0:
        print('Empty input directory!')
        exit(1)

    binlen = len(dirlist) / mp.cpu_count()

    for segment in chunks(dirlist, int(binlen)):
        p = mp.Process(target=gen_spectograms, args=(segment, args.input_dir, args.output_dir,))
        p.start()
        procs.append(p)

    for proc in procs:
        proc.join()

    end = time.time()

    print('Time: %fs, %fs/item' % (end - start, (end - start) / len(dirlist)))

if __name__ == '__main__':
    main()
