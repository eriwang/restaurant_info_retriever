# Restaurant Info Retriever

A general purpose project for myself to fetch info about restaurants and "do stuff" with it.

## Setup

### Development

This project is set up using virtualenvs. I'm using Python 3.8.3 since that's what I happen to have
installed, though other Python versions likely work as well.

```bash
python3 -m venv venv
source activate venv/bin/activate
pip install -r requirements.txt
```

Create a copy of `creds.example.json` and name it `creds.json` - this is where the application will
pull API keys from in development.

#### External Dependencies

This project uses various APIs that require some external setup.

Go to the Google Cloud console and set up a new project.

- Enable the Google Maps Platform API by following the instructions [here](https://developers.google.com/maps/get-started)
    - Note that you may need to enable a billing account for this
    - Save the API key to `creds.json` in the repo
