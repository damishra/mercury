```yaml
milestone:
    iteration: 07
    title: 'Deployment Packaging'
    date: 'April 30, 2021'
group:
    number: 06
    name: 'Mercury- The Data Delivery System'
    members:
        - 'Dishant Mishra, Vincent Cheng'
```

# Mercury - The Data Delivery System
## Project Description
Survey software has been heavily use for marketing purposes and research. We wanted to have a back-end API system, that would allow people to create their own set of applications with their own questions times and etc.

Mercury is the brainchild of Vincent Cheng and Dishant Mishra. We have been
frustrated with the numerous survey tools and products in the market and how
they do not offer the flexibility certain use cases demand. We decided to solve
the problem by coming up with an open ended API-only solution where the users
will only have to deal with four base data repositories - User, Survey,
Question, and Response. Question and Response are two highly malleable
repositories that allow users to create their own question types, and store
their responses. This is made possible thanks to postgres' flexible JSONB
datatype.

Think of this as a SaaS (Software as a Service), where we handle the auth and
storage, and the user does whatever they want with our flexible storage system.

## Project Requirement

-   Relational Database
-   API Queries
-   Object-Oriented Programming Language

## Technologies Used

-   Back-end
    -   ~~**MySQL/MariaDB, ExpressJS, NodeJS**~~
    -   Refactoring/Opted for FastAPI, Python/asyncio, PostgreSQL/asyncpg and supadb (remote database)
-   Front-end
    -   ~~**React.js**~~
    -   Opted for Python
-   GitHub
    -   GitHub URL: https://github.com/damishra/mercury

We have opted to go with python in this rewrite as this gives us access to
FastAPI, a library written almost entirely with speed in mind. It has it's
internals written in highly optimized C. It also supports asynchronization out
of the box, which makes it really appealing for handling high traffic on highly
used endpoints for the API.

### Performance and Refactoring

#### Performance

We have opted to go with python in this rewrite as this gives us access to
FastAPI, a library written almost entirely with speed in mind. It has it's
internals written in highly optimized C. It also supports asynchronization out
of the box, which makes it really appealing for handling high traffic on highly
used endpoints for the API.

Another reason is the fact that allows us to strongly type (I know I say that as
I use a duck-typed language) body and query parameters for the requests.

Another decision we made was use the non-standard asyncpg drivers to interact
with postgres. This driver is also highly optimized as it has its internals
written in Cython. This library allows us to use raw SQL asynchronously which is
good for optimizing reads.

#### Testing

We are using the inbuilt fastapi test client along with the pytest library to
test our crud functionality. Example code is in the `test_auth.py` file in the
project root.

To setup your environment, it is recommended to make a virtual environment in
the project root with venv: `python3 -m venv venv`, and then installing the
requirements with `pip install -r requirements.txt`.

To run the tests, use the `runme_win.ps1` file for powershell and the
`runme_nix.sh` file for bash/zsh.

Before running the script, remeber to add your own credentials in. The `JWTKEY`
can be left as is.

#### Refactoring - Design

One of the benefits of going with FastAPI is that it is design agnostic. This
allows us to use any design pattern we desire to organize our project. We
decided to go with an MVCesque domain-based patter where our routing is separate
from our models and controllers, which is desirable for modularity.

The project rewrite is allowing us to use postgres from the start with a high
performance specialized driver. Something that we were not able to find a good
replacement for in nodejs without using an orm based driver.


### Packaging and Deployment

Since this is almost an entirely pythonic project, packaging is a
non-requirement, and deployment is easy. The project is available at
<https://github.com/damishra/mercury>.

The minimum supported python version is v3.7. We recommend creating a virtual
environment with the venv module before installing the dependencies as this
project uses some default python packages that might cause issues with the OS's
python environment. The instructions to deploy are as follows:

#### Unix

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

#### Windows

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