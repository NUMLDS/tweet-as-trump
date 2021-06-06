.PHONY: image read process clean train remove

image:
	docker build -f Dockerfile -t tweets_pipeline .

data/pipeline/raw.csv:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY tweets_pipeline run.py pipeline read --output=data/pipeline/raw.csv

read: data/pipeline/raw.csv

data/pipeline/processed.csv: data/pipeline/raw.csv
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ tweets_pipeline run.py pipeline process --input=data/pipeline/raw.csv --output=data/pipeline/processed.csv

process: data/pipeline/processed.csv

data/pipeline/cleaned.csv: data/pipeline/processed.csv
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ tweets_pipeline run.py pipeline clean --input=data/pipeline/processed.csv --output=data/pipeline/cleaned.csv

clean: data/pipeline/cleaned.csv

train: data/pipeline/cleaned.csv
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ tweets_pipeline run.py pipeline train --input=data/pipeline/cleaned.csv

remove:
	rm -r data/pipeline
	mkdir data/pipeline
	touch data/pipeline/.gitkeep

all: image train remove
