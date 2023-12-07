aboships-dataset:
	@for split in train test val; do \
		python utils/make_annotation_info.py --input_file_path data/aboships/annotations/$$split.json --output_file_path data/aboships/labels/$$split/annotation_info.json; \
	done

	@for split in train test val; do \
		python utils/make_labels.py --input_file_path data/aboships/labels/$$split/annotation_info.json --output_directory data/aboships/labels/$$split/; \
	done

	@for split in train test val; do \
		python utils/rename_labels.py --input_directory data/aboships/labels/$$split/; \
	done

split-datasets:
	python dataloaders/split_aboships.py --source_folder data/aboships/ --destination_folder data/aboships/
	python dataloaders/split_simuships.py --images_folder data/simuships/images --labels_folder data/simuships/labels --output_folder data/simuships/ --train_size 0.7 --val_size 0.15 --test_size 0.15