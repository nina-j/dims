# DIMS · Data Ingestion Machine in Space ✨ 🚀

Welcome to DIMS!

## Quickstart
Add a `docker-compose.override.yml` with the following contents

```yml
services:
  dims:
    volumes:
      - /your/favourite/path:/code/data:rw
```
in order to access output files. Then

```bash
docker-compose run dims
```

You will be greeted with progress bars, and soon, four beautiful `.csv` files!

If you want to run DIMS locally, simply [install poetry](https://python-poetry.org/) and run

```bash
poetry install; poetry run dims
```

## Settings
A few things are configurable via environment variables, namely `bucket`, `output_dir` and `max_results`.
Changing the output directory might be useful if running DIMS locally. `max_results` controls the number of blobs returned from the bucket. For example:

```fish
docker-compose run -e MAX_RESULTS=5 dims
> Downloading data: 100%|████████████████████████████████████████████████| 5/5 [00:00<00:00, 49.08it/s]
> Parsing data: 100%|████████████████████████████████████████████████████| 5/5 [00:00<00:00, 28.49it/s]
> Outputting /code/data/LanderSaturn.csv: 100%|██████████████████████████| 5000/5000 [00:00<00:00, 98853.25it/s]
```

## Tests
This project has 100% test coverage (:sunglasses:). Tests can be run as follows

```
docker-compose run dims pytest --cov=dims
```

or, if installed locally

```
poetry run pytest --cov=dims
```

## Rationale
This project is equal parts a challenge and a playground.

I wanted to solve the small file problem _without_ using [`pandas`](https://pandas.pydata.org/), even though the csv parsing capabilities are virtually unmatched in Python. I also wanted to showcase the strength of [`pydantic`](https://pydantic-docs.helpmanual.io/) data models and thus opted to solve the problem almost entirely using these.

In addition, I wanted to try out pattern matching, new in Python 3.10, and therefore this project is only compatible with that version onwards.
Finally, I've been curious about conventional commits, and so this project is set up to use this commit pattern via [`pre-commit`](https://pre-commit.com/) and the [`commitizen`](https://commitizen-tools.github.io/commitizen/) hook.

## Issues & considerations

The most difficult part of this project was determining how to work with gcp client libraries, as I am unfamiliar and I find the documentation to be a bit lacking. As such, I am a little unsure if I actually succeeded in getting batches of a certain size. However, download of blobs works fine and is reasonably fast.

Speaking of speed... The parsing step is slower than I would have liked. I tried to fix this using multiprocessing pools, but had to make do with thread pools instead due to pickling issues. These suffer a bit under the GIL and are not really giving super great results. My thinking is that `pandas` might be more efficient in both space and time (my solution eats RAM like candy), but the challenge was to do without, so here we are.

Development wise, integration tests should have been utilised earlier in the process, as I discovered a few errors when coding the main module.

In conclusion, if I had to do this again, I would probably

- actually use `pandas` or another parser for csv-files
- still utilise `pydantic` models because I find they're great at describing data
- do integration tests sooner
- still use conventional commits, it's great!
