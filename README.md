# EnvSensingServer
This repostory contains the server-side source code of *Mobile Environment Sensing System*,
which is the subject of my final year project as an undergraduate course in year 4.

Under development

See also: [EnvSensingClient](https://github.com/sorz/EnvSensingClient)


## Deployment
0. Install Python 3;
   ```
   $ sudo apt-get install python3
   ```

1. Download source code;
    ```
    $ git clone https://github.com/sorz/EnvSensingServer.git
    $ cd EnvSensingServer/
    ```

2. Create and active virtual environment (optional);
   ```
   $ pyvenv env
   $ . env/bin/activate
   ```

3. Install requirements;
   ```
   $ pip install -f requirements.txt
   ```

4. Change configuration;
   ```
   $ cp config.py instance/config.py
   $ vim instance/config.py
   ```

5. Initialize database;
   ```
   $ ./run.py create_db
   ```

6. Install JavaScript libraries;
   ```
   $ ./run.py bower_install
   ```

7. Start server in debugging mode.
   ```
   $ ./run.py run
   ```

