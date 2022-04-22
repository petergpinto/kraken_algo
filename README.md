
This requires python-virtualenv and python-pip.
Setup python virual environment

```bash
mkdir my-project
cd my-project
# bootstrap virtualenv
export VIRTUAL_ENV=.virtualenv/krakenex
mkdir -p $VIRTUAL_ENV
virtualenv $VIRTUAL_ENV
source $VIRTUAL_ENV/bin/activate
# install from PyPI
pip install -r requirements.txt 
```

To activate the virtual environment on a new terminal session
```bash
export VIRTUAL_ENV=.virtualenv/krakenex
source $VIRTUAL_ENV/bin/activate
```

OR

```bash
source .virtualenv/krakenex/bin/activate
```
