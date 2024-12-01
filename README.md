# Financier

AI-powered personal finance management API

## ⚠️ Work in progress

As much as I love to work on this project fulltime, I still have a job that I love.

## 🧠 What is it?

Basically a glorified bookkeeper, financial coach, and financial manager.
I wanted to leverage the use of OpenAI models to create an assistant that will:

- keep track of my expenses
- generate reports
- remind me of a money-related event
- make me feel good about my financial health (or not)

### Features

1. 📃 Create, list, read, update, delete income and expense items.
2. 📸 Upload a photo of a receipt and let the assistant book it for you.
3. 📈 Generate daily, monthly, yearly reports of your finances.
4. 💪🏽Set budgets (daily and weekly).
5. 📨 Receive emails about alerts and notifications.
6. ⛰️ Set financial goals.
7. 👨🏽 Ask the assistant about your finances.

## Installation

1. Use `poetry` for the project.
2. Define `.env` with the following contents:

```
STAGE=<stage>
APP_NAME=<name>
PYTHON_PATH=${workspaceDirectory}
```

### Creating the Lambda layers

All the requirements are found in the `financier/functions_stack/layers` folder. We are using `pydantic` and there is a special build needed for it to make it working with Lambda.

```
pip install --platform manylinux2014_x86_64 --implementation cp --python-version 3.12 --only-binary=:all: --upgrade pydantic --target <directory>
```

Make sure to update this when you are using a new python package.

## Running Local Development

1. Enable your environment.
2. Go to `financier/functions_stack/`
3. Run local FastAPI development server,

```
fastapi dev fastapi_lambda.py
```

## Quality

The project uses: `isort`, `ruff`, and `black` for code formatting. I've created a `.bat` file to run the necessary steps.

```
runner.bat
```

This will be improved in the future as I am trying to make `tox` work for the project.

## 🛣️ Roadmap

### Phase 1

Initial setup.

- Initialize project structure
- Setup project
- Setup tests

### Phase 2

Simple proof of concept for data management.

- Data modelling
  - Expense
- Database stack
  - DynamoDB setup
- API stack
  - Create
  - Read
  - List
  - Update
  - Delete
- Lambda stack
  - Setup lambda layers
  - Create lambda layer creation script
  - Create
  - List
  - Read
  - Update
  - Delete
- Convert function creations to use YAML loading

### Phase 3

Securing our application.

- Stardardize IAM roles
- Cognito setup
  - Identity pools
- API Gateway authorizer

### Phase 4

Setup the assistant

- Write OpenAI model code for the assistant.
- Interface for the Financier API and the assistant API.

### Phase 5

Assistant features

- Tools for the assistant
  - Reports generator
  - Chat
  - Photo manager

### Phase 6

More assistant features

- Budget
- Alarms
- Goals
