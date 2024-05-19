# Bucks Bunny Web Application

## Purpose
Bucks Bunny is a simplified money tracking app designed to ease your financial journey. With Bucks Bunny, effortlessly monitor your monthly expenses and gain insights into your spending habits like never before.

## Objectives of the Web Application
Bucks Bunny revolutionizes personal finance by providing detailed insights into monthly spending and comprehensive yearly analyses. Our platform delivers personalized feedback and guidance, adapting to individual spending habits and financial aspirations.

## Team Members

| UWA ID    | Name                  | Github Username        |
|-----------|-----------------------|------------------------|
| 23981621  | Amrita Manoj          | amritamnj              |
| 23881368  | Rabi Ul Hasan         | DueDiligence21         |
| 23882963  | Zaid Sayed            | zaidsayed              |
| 24072387  | Vallabhaneni Sravani  | Sravanichowdary9       |

## Launch the Environment

### Create Virtual Environment
```bash
python3 -m venv .venv
```
This command creates a virtual environment named 'env' in your project directory.

### Activate Environment:
- **Mac**: 
  ```bash
   .venv/bin/activate
  ```
- **Windows**:
  ```bash
 .venv\Scripts\activate
```
This command activates the virtual environment.

```bash
pip install -r /requirements.txt
```
This command will read the requirements.txt file and install all the listed dependencies into your virtual environment. 

### Initialize the Database Migration Environment:
```bash
flask db init
```
### Create an Initial Migration:
```bash
flask db migrate -m "Initial migration"
```
### Apply the Migration to the Database:
```bash
flask db upgrade
```
### Run the Flask Server:
```bash
flask run
```
This command starts the Flask development server, allowing you to access your application.

### Note:
We have integrated the Group Dashboard with specific URL linking functionality. This integration aims to provide users with a seamless experience by directing them to their personalized group dashboard upon entering a designated URL. This feature will allow users to compare themselves with their friends and peers, fostering engagement and facilitating meaningful interactions within our platform.

We were successful in tracking the specific users' aggregated expenses and established tables for each functionality, but unfortunately, we were unable to do the specific URL linking to create a group dashboard.

```
