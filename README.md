# CS 411 Project: AcademicWorld ReadME


## Project Title:
Academic World: Explore Professors and Publications with Keywords


## Purpose:
This application aims to serve graduate students who would like to explore various research topics of interest, as well as relevant professors and publications, when writing their research papers.


## Demo:
[Video Demo Link](https://mediaspace.illinois.edu/media/t/1_on31glsa)


## Installation:
This application utilizes MySQL, MongoDB, and Neo4j databases. To install the application, first ensure that each of the three databases are running locally on their machine, with the Academic World data loaded into each. Then, download the python files (`mydash.py`, `mysql_utils.py`, `mongodb_utils.py`, `neo4j_utils.py`) and run `mydash.py` through a terminal command. This will produce a local host URL to access the dashboard.


## Usage:
The 6 widgets of the dashboard are arranged in a practical rectangular layout, and each widget uses straightforward user inputs to produce informative data displays. The user can find professors and publications relevant to their keyword of interest, examine the historical trends of keywords in publications, find highly-cited publications relevant to their keyword, explore the top research fields at a university of their interest, and also save their favorite faculty members and publications.


## Design:
The application relies on data from MySQL, MongoDB, and Neo4j databases. Each widget accesses one of these databases. Neo4j is used for the first and fourth widgets (find universities/professors for a given keyword and find top keywords for a given university, respectively). MongoDB is used for the third widget (find most-cited publications with a given keyword). MySQL is used for the second widget (historical trends for a given keyword) as well as the final two widgets, which compile favorite faculty and publications lists.


## Implementation:
The applications uses Python packages which contain tools for accessing the databases (`pymysql`, `pymongo`, `neo4j`) and written helper functions for performing tasks within the database (such as querying data, filtering results, and creating and updating tables). The application uses the `dash` framework for constructing the interface, `plotly.express` and `pandas` libraries for data visualization, and `dash_bootstrap_components` for styling and beautification.


## Database Techniques:

- **Prepared Statement**:
Prepared statements are used for each of the widgets and all 3 databases. For the respective database, a querying or updating statement is given with placeholders to be replaced by the user's input(s), and executed when the dashboard is in use.

- **Transaction**: 
The transaction method is used for widget 5 and 6 in `mysql_utils.py`, for creating, updating, and deleting favorite faculty and publications. We create a table if it doesn’t exist in the database and add the data, updating the table. The queries are executed together as a block of work and committed as a transaction.

- **Index**:
Indexes are created in `mysql_utils.py` as “keyword name”, “faculty name”, and “publication title”, in the “keyword”, “faculty”, and “publication” tables, respectively. These indices speed up the performance of MySQL select statements (widgets 2, 5, 6). See below:
![image 1](/index_sample_image.png)


## Contributions: 
- Brainstorm ~ Arjun Kshirsagar, Chang Hun Park (04/03 - 04/07)
- Constructing Widgets 1-4 (Querying Widgets) ~ Chang Hun Park (04/10 - 04/16)
- Constructing Widgets 5-6 (Updating Widgets) ~ Chang Hun Park, Arjun Kshirsagar (04/17 - 04/20)
- Beautification ~ Arjun Kshirsagar (4/20 - 4/21)
- Readme/Video ~ Arjun Kshirsagar, Chang Hun Park (04/23 - 04/25)
