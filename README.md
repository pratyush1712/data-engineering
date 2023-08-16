# Cornell Innovation and Entrepreneurship - Data Analysis Platform

Centralized data analysis platform for the Cornell Innovation and Entrepreneurship Lab. This repository contains scripts for data collection, data cleaning, and data analysis.

## Getting Started

### Prerequisites

- Python 3.9
- pip
- virtualenv
- Cornell Email

### Installation

1. Clone the repository

```bash
git clone
```

2. Create a virtual environment

```bash
virtualenv venv
```

3. Activate the virtual environment

```bash
source venv/bin/activate
```

4. CD into the server repository

```bash
cd server
```

5. Install the dependencies

```bash
pip install -r requirements.txt
```

6. Create a .env file in the server directory

```bash
touch .env
```

7. Add the following environment variables to the .env file

```bash
export CORNELL_NETID = "your_cornell_netid"
export CORNELL_PASSWORD = "your_cornell_password"
export CAPITAL_IQ_USERNAME = "your_capital_iq_username"
export CAPITAL_IQ_PASSWORD = "your_capital_iq_password"
```

8. Source the .env file

```bash
source .env
```

9. Run the server

```bash
python app.py
```

10. Open a new terminal window and CD into the client repository

```bash
cd cornell-data
```

11. Install the dependencies

```bash
npm install
```

12. Run the client

```bash
npm start
```

## Usage

The platform could be used to collect companies data in the following ways:

1. Collecting data of list of companies from Capital IQ, Mergent Intellect, or Guidestar websites, individually.

```bash
cd scraping
```

```bash
python index.py --source
```

2. Collecting data of list of companies from Capital IQ, Mergent Intellect, or Guidestar websites, in bulk.

```bash
python index.py
```
