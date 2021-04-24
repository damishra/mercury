```yaml
milestone:
    iteration: 06
    title: "Testing"
    date: "April 23, 2021"
group:
    number: 06
    name: "Mercury- The Data Delivery System"
    members:
    - "Dishant Mishra, Vincent Cheng"
```  
  
# Mercury - The Data Delivery System
## Project Requirement
- 24/7 Shared Server
- Relational Database 
- API Queries
- Object-Oriented Programming Language

## Technologies Used  
- Back-end
     - ~~**MySQL/MariaDB, ExpressJS, NodeJS**~~
     - Refactoring/Opted for Postgres, FastAPI, Python
- Front-end 
     -  **React.js** 
     -  **BootStrap**
- GitHub
    - ~~GitHub URL: https://github.com/europa-report~~
    - GitHub URL: https://github.com/damishra/mercury

### Performance and Refactoring

#### Performance
We have opted to go with python in this rewrite as this gives us access to FastAPI, 
a library written almost entirely with speed in mind. It has it's internals written 
in highly optimized C. It also supports asynchronization out of the box, which makes 
it really appealing for handling high traffic on highly used endpoints for the API.

Another reason is the fact that allows us to strongly type (I know I say that as I 
use a duck-typed language) body and query parameters for the requests. 

Another decision we made was use the non-standard asyncpg drivers to interact 
with postgres. This driver is also highly optimized as it has its internals written in 
Cython. This library allows us to use raw SQL asynchronously which is good for 
optimizing reads.
[..\mercury\readme.md](..\mercury\readme.md)


#### Refactoring - Design
One of the benefits of going with FastAPI is that it is design agnostic. This allows us
to use any design pattern we desire to organize our project. We decided to go with 
an MVCesque domain-based patter where our routing is separate from our models and 
controllers, which is desirable for modularity.

The project rewrite is allowing us to use postgres from the start with a high 
performance specialized driver. Something that we were not able to find a good 
replacement for in nodejs without using an orm based driver.

### Testing
We are using the inbuilt fastapi test client along with the pytest library to
test our crud functionality. Example code is in the `test_auth.py` file in the
project root.

Before running the script, remeber to add your own credentials in. The `JWTKEY`
can be left as is.

####Test Script Configuration
To setup your environment, it is recommended to make a virtual environment in
the project root with venv: `python3 -m venv venv`, and then installing the
requirements with `pip install -r requirements.txt`.

#### Running the Test
To run the tests, use the `runme_win.ps1` file for powershell and the
`runme_nix.sh` file for bash/zsh.

