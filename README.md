# Considerations & notes
* Most of the tasks could be completed using basic SQL queries. I'm unsure what's the expectation regarding this exercise (more programming oriented, therefore a more complete solution is welcome; or more system design oriented, where the right call would be to set up a script to use the CSV files as the source of truth, transform them to database rows, and utilise SQL to perform the queries).
* Due to simplicity, no multi-stage Docker containers are used.
* "tests" is not a real service, nor is it a good candidate to be one. Added it for ease of use when evaluating the solution.
* Code formatting is delegated to [Black](https://github.com/psf/black)

# Running the application

`docker-compose up app` will take care of building and starting the application

`docker-compose run --rm tests` will build the container if it doesn't exist and run the tests