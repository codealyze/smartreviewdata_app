import subprocess

if __name__ == '__main__':
	#subprocess.call("python ./object_detection/acc_rtn_images/push_tf_records.py", shell=True)
	subprocess.call("export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim", shell=True)
	subprocess.call("protoc object_detection/protos/*.proto --python_out=.", shell=True)	
	subprocess.call("gcloud ml-engine jobs submit training `whoami`_object_detection_`date +%s` --job-dir=gs://smartreviewdata/acc_rtn_images/train --packages dist/object_detection-0.1.tar.gz,slim/dist/slim-0.1.tar.gz --module-name object_detection.train --region us-central1 --config object_detection/samples/cloud/cloud.yml -- --train_dir=gs://smartreviewdata/acc_rtn_images/train --pipeline_config_path=gs://smartreviewdata/acc_rtn_images/data/digits_pipeline.config", shell=True)
