# Packaging and Deployment

Since this is almost an entirely pythonic project, packaging is a
non-requirement, and deployment is easy. The project is available at
<https://github.com/damishra/mercury>.

The minimum supported python version is v3.7. We recommend creating a virtual
environment with the venv module before installing the dependencies as this
project uses some default python packages that might cause issues with the OS's
python environment. The instructions to deploy are as follows:

### Unix

```bash
$bash[damishra::/home] git clone https://github.com/damishra/mercury.git
$bash[damishra::/home] cd ./mercury
$bash[damishra::/home/mercury] python3.7 -m venv venv
$bash[damishra::/home/mercury] source ./venv/Scripts/activate
(venv) $bash[damishra::/home/mercury] pip install -r requirements.txt
# make sure to edit runme_nix.sh before the next command...
(venv) $bash[damishra::/home/mercury] sh runme_nix.sh
(venv) $bash[damishra::/home/mercury] uvicorn mercury.main:app
# the project is now deployed on port 8000
```

### Windows

```powershell
PS C:\Users\damishra\Desktop> git clone https://github.com/damishra/mercury.git
PS C:\Users\damishra\Desktop> cd ./mercury
PS C:\Users\damishra\Desktop\mercury> python -m venv venv
PS C:\Users\damishra\Desktop\mercury> .\venv\Scripts\Activate.ps1
(venv) PS C:\Users\damishra\Desktop\mercury> pip install -r requirements.txt
# make sure to edit runme_win.ps1 before the next command...
(venv) PS C:\Users\damishra\Desktop\mercury> .\runme_win.ps1
(venv) PS C:\Users\damishra\Desktop\mercury> uvicorn mercury.main:app
# the project is now deployed on port 8000
```
