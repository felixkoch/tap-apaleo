# tap-apaleo

`tap-apaleo` is a Singer tap for apaleo.

The `tap-apaleo` extractor pulls data from the [apaleo API](https://api.apaleo.com/) into [Singer](https://singer.io) based ETL-pipelines, e.g. [Meltano](https://meltano.com).

Synchronise your booking data from apaleo with your data warehouse and build your own revenue KPI and reports in your business intelligence solution.

## Roadmap

- [x] Properties
- [x] Reservations
- [x] UnitGroups
- [x] Units
- [x] RatePlans
- [x] Maintenances

## Installation

### Using pipx

```bash
pipx install git+https://github.com/felixkoch/tap-apaleo.git
```

### Using pip3

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install git+https://github.com/felixkoch/tap-apaleo.git
```

## Configuration

### Using JSON

```shell
tap-apaleo --config config.json
```

where `config.json` is

```json
{
  "start_date" : "2017-01-01T00:00:00Z",
  "client_id": "<apaleo-client-id>",
  "client_secret": "<apaleo-client-secret>"
}
```

### Authentication and Authorization

Please refer to the apaleo developer documentation on [how to register a OAuth simple client application](https://apaleo.dev/guides/start/oauth-connection/register-app#register-the-oauth-simple-client-application) to get the `client-id` and `client-secret`.

The following scopes must be activated:
`maintenances.read, rateplans.read-corporate, reservations.read, setup.read`

Alternatively (or if you do not have a developer account) you can use the following link to set up a corresponding client in your account:

https://app.apaleo.com/apps/connected-apps/create?clientCode=TAPAPALEO&clientName=tap-apaleo&secret=tap-apaleo%20is%20a%20Singer%20tap%20for%20apaleo.&clientScopes=%5B%22maintenances.read%22,%22rateplans.read-corporate%22,%22reservations.read%22,%22setup.read%22%5D&piiMode=Retrieve

### Other

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-apaleo --about
```

## Usage

You can easily run `tap-apaleo` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-apaleo --version
tap-apaleo --help
tap-apaleo --config CONFIG --discover > ./catalog.json
```


### Example: Meltano Pipeline with Postgres (recommended)

1. Setup Meltano & initialize Meltano project

```bash
mkdir meltano-projects
cd meltano-projects
python3 -m venv .venv
source .venv/bin/activate
pip3 install meltano

meltano init apaleo-pipeline
cd apaleo-pipeline
```

2. Edit meltano.yml, add:

```yaml
plugins:
  extractors:
  - name: tap-apaleo
    namespace: tap_apaleo
    pip_url: git+https://github.com/felixkoch/tap-apaleo.git
    executable: tap-apaleo
    capabilities:
    - state
    - catalog
    - discover
    config:
      start_date: '2017-01-01T00:00:00Z'
    settings:
    - name: client_id
    - name: client_secret
      kind: password
    - name: start_date
      value: '2017-01-01T00:00:00Z'
```

3. Install & configure tap-apaleo

```bash
meltano install
meltano config tap-apaleo set client_id <apaleo-client-id>
meltano config tap-apaleo set client_secret <apaleo-client-secret>
```

4. Install & configure target-postgres

```bash
meltano add loader target-postgres
meltano config target-postgres set postgres_host localhost
meltano config target-postgres set postgres_port 5432
meltano config target-postgres set postgres_database postgres
meltano config target-postgres set postgres_username postgres
meltano config target-postgres set postgres_password example
meltano config target-postgres set postgres_schema public
```

5. Run & schedule ETL pipeline

```bash
meltano elt tap-apaleo target-postgres --job_id=apaleo-to-postgres

meltano schedule apaleo-to-postgres tap-apaleo target-postgres @hourly
meltano add orchestrator airflow
meltano invoke airflow scheduler
```

6. Read about [Deployment in Production](https://meltano.com/docs/production.html#your-meltano-project).

### Example: Singer Pipeline with Postgres

`tap-apaleo-conf.json`:

```json
{
  "start_date" : "2017-01-01T00:00:00Z",
  "client_id": "<apaleo-client-id>",
  "client_secret": "<apaleo-client-secret>"
}
```

`target-postgres-conf.json`:

```json
{
  "postgres_host": "localhost",
  "postgres_port": 5432,
  "postgres_database": "postgres",
  "postgres_username": "postgres",
  "postgres_password": "example",
  "postgres_schema": "public"
}
```

`state.json`:
```json
{}
```

#### With pipx

```bash
pipx install git+https://github.com/felixkoch/tap-apaleo.git
pipx install singer-target-postgres

tap-apaleo --config tap-apaleo-conf.json --state state.json | target-postgres --config target-postgres-conf.json >> state.json

tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
```
#### With pip3

Install each Tap and Target in a separate Python virtual environment. This will insure that you won't have conflicting dependencies between any Taps and Targets.

```bash
mkdir tap-apaleo
cd tap-apaleo
python3 -m venv .venv
source .venv/bin/activate
pip3 install git+https://github.com/felixkoch/tap-apaleo.git
deactivate
cd ..

mkdir target-postgres
cd target-postgres
python3 -m venv .venv
source .venv/bin/activate
pip3 install singer-target-postgres
deactivate
cd ..

./tap-apaleo/.venv/bin/tap-apaleo --config tap-apaleo-conf.json --state state.json | ./target-postgres/.venv/bin/target-postgres --config target-postgres-conf.json >> state.json
tail -1 state.json > state.json.tmp && mv state.json.tmp state.json
```

## Consulting / Hosting / Open for work
I'm a freelance Full Stack Developer & Data Analyst from near Hamburg. I can help you with setting up or hosting the data pipeline and creating meaningful reports in Power BI. Please get in touch:

Felix Koch  
felix@tagungshotels.info  
+49 4266 999 999 9  
[Make an appointment](https://meetings.hubspot.com/felix137)  
[https://felixkoch.de](https://felixkoch.de)  
[Imprint](https://tagungshotels.info/impressum)


## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_apaleo/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-apaleo` CLI interface directly using `poetry run`:

```bash
poetry run tap-apaleo --help
```
