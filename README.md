# Audio Capctcha classification

## General

This was a project for a university module on scalable computing. We had to generate and classify captchas as generated by commercial TTS engines (not _real_ captchas of course). train.py and classify.py are largely not my own work, the sources are indicated in the files.

Sample captchas are obtained en masse from AWS and GCP tts engines, they are then converted to a spectogram format using Sox, and then fed into a Tensorflow model to be trained.

## Requirements and installation

 * Python 3.7.4 containing the Pip packages in requirements.txt, use ```pip install -r requirements.txt```.
 * Sox, see http://sox.sourceforge.net (accessed 6th November 2019), can be installed using most package managers (I use Homebrew).
 * An AWS and GCP account for generating TTS samples. Credentials should go into ```gcp.json``` and ```aws_creds.py``` respectively. ```aws_creds.py``` should contain three strings only; ```aws_access_key_id```, ```aws_secret_access_key```, and ```region_name``` (e.g. 'eu-west-1').