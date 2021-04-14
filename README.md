# StateMachineJoint
This is an example Design studio aimed for developers relatively new to the [WebGME](https://webgme.org) platform.
It allows model editing, simulation, and some limited model-checking functionality.
The studio implements the finite state machine domain.
For its special simulator visualization, it uses the [JointJS](https://www.jointjs.com/) javascript library.

## Installation
First, install the StateMachineJoint following:
- [NodeJS](https://nodejs.org/en/) (LTS recommended)
- [MongoDB](https://www.mongodb.com/)

Second, start mongodb locally by running the `mongod` executable in your mongodb installation (you may need to create a `data` directory or set `--dbpath`).

Then, run `webgme start` from the project root to start . Finally, navigate to `http://localhost:8888` to start using StateMachineJoint!
