# roboboat2024

## Set up

This codebase is developed and tested on `python=3.8.10`.

- Clone this repository
- Download [`test_data/`](https://photos.app.goo.gl/y2SMzxv5S6S4NbCj6) and move it to `test_data/`


### Repo Structure

The following repo structure is from [robosub_2023](https://github.com/InspirationRobotics/robosub_2023).

`cv/`, `test_data`, `tests/` are currently implemented in this development branch. 

**Repo Structure is subject to change.**

```bash
roboboat2024
├── asv
│   ├── device
│   │   ├── # everything related to the sensors
│   │   ├── # each device should have its own file/folder
│   ├── localization 
│   │   ├── # TODO
│   ├── mission 
│   │   ├── # Mission classes
│   │   ├── # see asv/mission/template_mission.py for an example
│   ├── motion
│   │   ├── # Actuators code
│   │   ├── # each actuator should have its own file/folder
│   ├── cv
│   │   ├── # All CV classes and functions
│   │   ├── # see asv/cv/template_cv.py for an example
│   ├── utils
│   │   ├── # utility functions
├── scripts
│   ├── # bash scripts
├── mission
│   ├── # Mission files (calling mission classes)
├── tests
│   ├── # Unit tests (pytest)
├── config.json # where all the config values used in mission files are stored
├── setup.py # setup file for pip install
├── .gitignore
├── README.md
```

### Running

#### Tests

This will run all the tests in the tests folder using `pytest`.
Any file that has the name `test_*.py` will be run.

```bash
pytest
```

#### CV

The idea behind the CV classes is that they are run in a separate thread and they publish their results to a ROS topic.
You can run individually CV classes for debugging purpose (if they have a `if __name__ == "__main__"` block) by running:

```bash
python3 -m asv.cv.<cv_name>
```

## Contributing

### Unit Tests

We use pytest for unit tests. Please write unit tests for your code and make sure that they pass before pushing your code.
This is to make sure that we don't break anything when we add new features.
Tests are mainly there to make sure that there is no syntax error and that the code runs without crashing, not necessarily to make sure that the code is doing what it is supposed to do (although it is a plus).

### Code Style

It is always pleasant to read code that is well formatted and well commented.
Ideally we would want to format our code using black, so try to run regularly on your code:

```bash
black .
```

If you have trouble running this command, you can use the following command instead:

```bash
python3 -m black .
```