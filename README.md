# Audio Capctcha classification

## General

This was a project for a university module on scalable computing. We had to generate and classify captchas as generated by commercial TTS engines (not _real_ captchas of course). train.py and classify.py are not my own work save for minor modifications, the sources are indicated in the files.

Sample captchas are obtained en masse from AWS and GCP TTS engines, they are then converted to a spectogram format using Sox, and then fed into a Tensorflow model to be trained.

## Requirements and installation

 * Python 3.7.4 containing the Pip packages in requirements.txt, use ```pip install -r requirements.txt```.
 * Sox, see http://sox.sourceforge.net (accessed 6th November 2019), can be installed using most package managers (I use Homebrew).
 * An AWS and GCP account for generating TTS samples. Credentials should go into ```gcp.json``` and ```aws_creds.py``` (that file needs to be created by you) respectively. ```aws_creds.py``` should contain three strings only; ```aws_access_key_id```, ```aws_secret_access_key```, and ```region_name``` (e.g. 'eu-west-1').

## Usage

Type ```python programme.py --help``` for specific usage.

An example workflow for building a classification model is as follows, assuming ```gcp_key.json``` and ```aws_creds.py``` have already created:

 * Create two folders, ```test```, ```train```, ```test_spec```, and ```train_spec```
 * Run ```python makeaudio.py  --symbols charset.txt --length 8 --count 100000 --test_dir test --train_dir train```
 * Run ```python makespec.py --input_dir train --output_dir train_spec```
 * Run ```python makespec.py --input_dir test --output_dir test_spec```
 * Run ```python train.py --length 8 --symbols charset.txt --batch-size 4 --epochs 2 --output-model model --train-dataset train_spec --validate-dataset test_spec```

 The model can now be tested to classify captchas, try with

 * ```python classify.py  --model-name test --captcha-dir test/ --output ans.txt --symbols charset.txt```