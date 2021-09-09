# tap-apaleo

`tap-apaleo` is a Singer tap for apaleo.

## Note
This is still work in progress. Do not use in production. Please get in touch.

## Roadmap

- [x] Properties
- [ ] Reservations
- [ ] UnitGroups
- [ ] Units
- [ ] RatePlans
- [ ] Maintenances

## Installation

### Using pipx

```bash
pipx install git+https://github.com/felixkoch/tap-apaleo.git
```

### Using pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/felixkoch/tap-apaleo.git
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

### Source Authentication and Authorization

Please refert to the apaleo developer documentation on [how to register a OAuth simple client application](https://apaleo.dev/guides/start/oauth-connection/register-app#register-the-oauth-simple-client-application) to get the `client-id` and `client-secret`.

The following scopes must be activated:
`maintenances.read, rateplans.read-corporate, reservations.read, setup.read`

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

## Links
[apaleo](https://apaleo.com)


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
