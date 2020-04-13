# Bruce
One Command To Rule Them All

## Getting Started

### Write a Bruce.toml 
This where you decribe the different tasks you want bruce to run for you. 

You can currently define 4 kind of objects:

#### Tasks
A task wraps an actual command that you want run. Here is an example of a task wrapping the formatting tool [black](https://github.com/psf/black):
```toml
[task.black]
cmd = "venv/bin/black src/python --exclude venv bruce.py"
watch = ["py"]
upstream = ["deps"]
```

Let's break this example down:
- `[task.black]`, with this we define a task named `black`.
- `cmd = "venv/bin/black src/python --exclude venv bruce.py"`, we then define the command (`cmd`) to be run when we invoke this task.
- `watch = ["py"]`, here we describe the objects we want to watch. When a watch object changes, bruce understands that we will need to rerun the command on the next invocation of this task. We will go into more details about watchable objects later. This key is optional.
- `upstream = ["deps"]`, upstream is a the tasks that need to be executed before the current task is executed. In this example we point to a deps task, if you look at the [full example](https://github.com/OniOni/bruce/blob/master/Bruce.toml) you can see the `deps` task makes sure the project dependencies are installed. This key is also optional.  

#### Groups
A group is a task, but it has no command. It's mostly usefull for creating a new pseudo task grouping tasks that you often run together. Here's an example:
```toml
[group.qa]
upstream = ['mypy', 'black', 'isort']
```

In this example we create a group called `qa`. This let's you invoke those 3 tasks with `./bruce.py qa` rather than `./bruce.py mypy, black isort`. But those two commands are equivalent.

#### Files
A file, wraps, well a file. Once you've defined a file, you can then add it to the list of objects you want to `watch` in you task objects. Let's look at an example:  

```toml
[file.reqs]
fingerprintingstrategy = 'content'
path = 'requirements.txt'
```

Let's break this down:
- `[file.reqs]`: We're defining a file named `reqs`. The name is important as it's how we'll reference this object when we want to add it to the `watch` key on a task.
- `fingerprintingstrategy = 'content'`: This defines how bruce will determine if the file has changed. We currently support two strategies. The first on is `content`, where we examine the files content. The second one is `timestamp`, here we don't examine the content but rather the latest touch time to determine if a file has "changed". 
- `path = 'requirements.txt'`: This is the path of the file we're wrapping. 

#### Globs
Globs are a more general version of the file objects. The main difference here is, that rather than pointing to a single file, we pass in a glob. This allows us to watch many files. Heres' an example:
```toml
[glob.py]
fingerprintingstrategy = 'content'
glob = '**/*.py'
exclude = ['.*venv.*', '\.bruce/.*']
```

Here we define a glob called `py`. You might recall that this was the object we we're watching in our [task](#tasks) example above. Let's quickly call out the differences with `file` objects.
`glob`: This key expects a glob defining the files you want to be part of this object.
`exclude`: this is a list of globs of files you want excluded from the files wrapped by this object.


### Install
[![asciicast](https://asciinema.org/a/BGg2bU9B2KdKUAZI1wCe4BhpT.svg)](https://asciinema.org/a/BGg2bU9B2KdKUAZI1wCe4BhpT)

### Execute commands
[![asciicast](https://asciinema.org/a/dLCJoyEejwWepD4emaffR28GJ.svg)](https://asciinema.org/a/dLCJoyEejwWepD4emaffR28GJ)
```
