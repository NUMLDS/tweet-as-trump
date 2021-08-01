.PHONY: image database read process clean train remove pipeline test app tweet

image:
	docker build -f Dockerfile -t image .

database: image
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ image python3 run.py create_db

data/pipeline/raw.csv:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ image python3 run.py pipeline read --output=data/pipeline/raw.csv

read: data/pipeline/raw.csv

data/pipeline/processed.csv: data/pipeline/raw.csv
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ image python3 run.py pipeline process --input=data/pipeline/raw.csv --output=data/pipeline/processed.csv

process: data/pipeline/processed.csv

data/pipeline/cleaned.csv: data/pipeline/processed.csv
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ image python3 run.py pipeline clean --input=data/pipeline/processed.csv --output=data/pipeline/cleaned.csv

clean: data/pipeline/cleaned.csv

train: data/pipeline/cleaned.csv
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ image python3 run.py pipeline train --input=data/pipeline/cleaned.csv

remove:
	rm -r data/pipeline
	mkdir data/pipeline
	touch data/pipeline/.gitkeep

pipeline: image train remove

test:
	docker run image pytest

app:
	docker build -f app/Dockerfile -t tweets_app .

tweet: app
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ -p 5000:5000 tweets_app
