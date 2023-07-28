
### usage
```
win cmd >
set RUNPY=has-root
set DOWNURL=https://github.com/nblog/cloud-py3-example/blob/main/%RUNPY%.py?raw=true
set NOSSL=import ssl;ssl._create_default_https_context=ssl._create_unverified_context;
python -c "%NOSSL%import urllib.request;HTTPGET=urllib.request.urlopen;exec(HTTPGET('%DOWNURL%').read().decode('utf-8'))"
```

```
linux shell >
export RUNPY=has-root
export DOWNURL=https://github.com/nblog/cloud-py3-example/blob/main/${RUNPY}.py?raw=true
export NOSSL="import ssl;ssl._create_default_https_context=ssl._create_unverified_context;"
python3 -c "${NOSSL}import urllib.request;HTTPGET=urllib.request.urlopen;exec(HTTPGET('${DOWNURL}').read().decode('utf-8'))"
```

### quick python (windows)
```
cmd >
curl -L https://github.com/nblog/cloud-py3-example/raw/main/win-install-py3.cmd -o install-py3.cmd && CALL install-py3.cmd
```