
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


Crontab entry for updating tradable pairs daily
```cron
0   1 * * *     /home/peter/kraken/.virtualenv/krakenex/bin/python /home/peter/kraken/get-all-tradable-pairs.py
```


Simple moving average SQL
```sql
SELECT a.timestamp, a.open, 
	Round( 
		( select SUM(b.open) / count(b.open) 
		FROM ohlc_data as b WHERE TIMEDIFF(a.timestamp, b.timestamp) 
		BETWEEN 0 AND 10
		), 2) as '10MinuteMovingAvg' 
	FROM ohlc_data as a 
	order by a.timestamp;
```



## Currency codes meaning
XBT is BTC

XXBTZUSD is a currency pair that represents BTC/USD

X denotes crypto
Z denotes cash

https://support.kraken.com/hc/en-us/articles/360001185506-How-to-interpret-asset-codes
https://support.kraken.com/hc/en-us/articles/360001206766-Bitcoin-currency-code-XBT-vs-BTC



## Automated Trading

### Strategies

#### SMA Cross

	BUY: SMA30 goes above SMA200
	SELL: SMA30 goes below SMA200
