super simple script for using a webcam as a security camera.

Grabs frames from the webcam and uploads them to an S3 bucket
regularly.

To save bandwidth, it uses very simple motion detection. If there is
motion detected, it uploads one frame per second (roughly; depends on
how long it takes to access the webcam device). No motion detected and
it only uploads once per minute (mostly so you can easily tell that
the script is still running).

The S3 bucket is set up with a lifecycle policy to delete files that
are more than 21 days old. That should keep the storage costs very
low.

Currently, this is all hard coded to my own setup. If you want to run
this yourself, you will need an S3 bucket set up the same way, the AWS
CLI installed and configured with credentials that will allow you to
write files to the bucket (and ideally, for an IAM role that does not
have permissions to delete files from the bucket). And you will need
the python requirements specified in `requirements.txt` installed
(plus any system-level dependencies that they have).

The variables at the top of the script would need to be adjusted based
on your particular circumstances (it will probably take some
experimentation to see what threshold works well for you).
