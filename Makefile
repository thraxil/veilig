install:
	python3 -m venv ve
	./ve/bin/pip install wheel
	./ve/bin/pip install -r requirements.txt

create_bucket:
	/usr/local/bin/aws s3api create-bucket --bucket thraxil-veilig --acl private
	/usr/local/bin/aws s3api put-bucket-lifecycle-configuration --bucket thraxil-veilig --lifecycle-configuration file://lifecycle.json

get_images:
	/usr/local/bin/aws s3 cp s3://thraxil-veilig/ /tmp/veilig/ --recursive
