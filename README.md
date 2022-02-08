# Considerations & notes
* Most of the tasks could be completed using basic SQL queries. I'm unsure what's the expectation regarding this exercise (more programming oriented, therefore a more complete solution is welcome; or more system design oriented, where the right call would be to set up a script to use the CSV files as the source of truth, transform them to database rows, and utilise SQL to perform the queries).
* Due to simplicity, no multi-stage Docker containers are used. Also using alpine as build-times aren't a concern at this moment. If they'd be, I'd recommend switching to a multi-stage build with "bullseye-slim" as the builder, and whatever fits the application's needs for a runtime container.
* "tests" is not a real service, nor is it a good candidate to be one. Added it for ease of use when evaluating the solution.
* Code formatting is delegated to [Black](https://github.com/psf/black)
* I'm sacrificing performance for readability. In my opinion the dataset could grow significantly, and the naïve approach I've taken should support that. Also if it'd be a real concern, I'd recommend changes in the system design (use a database) to support a more efficient approach.
* I've spent a considerable amount of time building a TUI, which I've abandoned due to it being a waste of everyone's time. The main entrypoint now generates all reports without any interactive user interface.

# Running the application

`docker-compose run --rm app` will take care of building and starting the application

`docker-compose run --rm tests` will build the container if it doesn't exist and run the tests

# Project structure

`core` contains the core application logic. The only constraint that should apply here is the language itself. It should be agnostic of everything else (like whether there's a database, or any kind of persistent storage, whether it's a web app or a CLI, etc).

`core` should use drivers or plugins to interact with the rest of the application. There should be an interface or abstract class that defines the interface. This should ensure a basic level of compatibility between different drivers/plugins that implement the interface or inherit from the class.

`data` holds the input files.

`output` is the destination for report generation. It's bound using a volume in docker-compose. If you aren't using that to run the script, you'll either manually have to specify the mount, or browse the files from within the container.