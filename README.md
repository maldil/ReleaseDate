# ReleaseDate
STM solver to decide release date

Continuous delivery (CD) is a software engineering approach in which teams produce software in short cycles, ensuring that the software can be reliably released at any time. 
The frequent release process that provides incremental updates to applications in production improves client satisfaction greatly. 
Therefore, carefully deciding the release dates up to the final release date is always a NP hard problem due to the complex requirements.
Requirements may include:
(i) some features (i.e, bug fixes or new functionalities) should be started before others, (ii) some features can not be implemented parallelly, (iii) some features can only be implemented by particular developers, or (iv) some features can not be implemented parallelly due to resource unavailability.


## Steps to run the docker image

1. Install Docker (If you do not have).
2. Use the command "docker version" to make sure that you have installed Docker correctly.
3. Run "docker pull shashidoo1990/releaseprob:latest" to pull the image to local machine.
4. Run "docker run shashidoo1990/releaseprob:latest" to run the test cases mentioned in "https://github.com/maldil/ReleaseDate/blob/master/PROJECT/release_data.json".


## Steps to build the project from scrach. 
1. execute "git clone https://github.com/maldil/ReleaseDate.git"
2. "cd ReleaseDate"
3. Make a Python virtual environment or open the project using an IDE (e.g., PyCharm)
4. Turn on your virtual environment
5. "cd PROJECT"
6. Execute "pip install -r requirements.txt" to install all the libraries (i.e. PySMT==0.9.0, tqdm==4.46.1, z3-solver==4.8.8.0)
7. Execute "python release_main.py"
8. You can add new test cases to the release_data.json
