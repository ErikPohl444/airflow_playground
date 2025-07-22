# Airflow Playground

A playground for learning Apache Airflow, based on an outdated tutorial that required significant fixes and modernizations. The process of updating and repairing the DAGs provided valuable hands-on experience in troubleshooting and adapting Airflow pipelines.

## Features

This repo includes:

- Example Airflow DAGs and supporting Python scripts
- Updated code and configurations to work with current Airflow versions
- Notes and comments on common problems faced and how they were fixed

## Future plans

- [ ] Add more advanced Airflow examples
- [ ] Document troubleshooting steps in greater detail
- [ ] Move future plans to issues

## Important disclaimer

This is a personal learning project. For more interesting work, see my Hello, World root readme.

## Getting Started

Clone the repo and explore the sample Airflow DAGs.

## Prerequisites

- Python 3.7+
- Apache Airflow (latest version recommended)
- See `requirements.txt` for dependencies

## Installing

1. Clone the repo
2. Set up a Python virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Initialize Airflow: `airflow db init`
5. Create a user and start the webserver/scheduler as per Airflow docs
6. Confirm $AIRFLOW_HOME is set to the airflow_playground folder.
7. Check the airflow.cfg file for paths to the dags folder and other paths.

## Running the tests

Testing is not yet automated for these DAGs. You can manually trigger DAG runs from the Airflow UI to validate their behavior.

## Contributing

Pull requests are welcome! There are no formal contributing rules at this time.

## Authors

- **Erik Pohl** - *Initial work*

Also see the list of GitHub contributors.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Thanks to everyone who has motivated me to learn more.
