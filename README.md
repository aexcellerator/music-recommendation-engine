# music-recommendation-engine
A local music recommendation engine
## requirement list:
- libraries/tools: 
    1. Embedding Generator: https://github.com/IBM/MAX-Audio-Embedding-Generator to create Embeddings of audio files
    2. pandas, numpy
    3. sklearn to find music which embedding is alike using approximate nearest neighbors (alternatively we will be using annoy, a library which is specified to do just that)
    4. matplotlib, seaborn (eventually to visualize relations between music)
    5. pydup, ffmpeg (for music file conversion)

- step-by-step list
    1. get a batch of music files convert them automatically into the appropriate format and extract their metadata
    2. use the embedding generator to generate embeddings of these
    3. the user then can input a music file in the application via command line
    4. the user gets a recommendation based upon the nearest neighbor found (the user can also specify how many nearest neighbors should be suggested)

- processing files:
    1. music\_preprocessing.py [input: a music file of various formats (which are able to be parsed by pydub)/a list of files; output: a formatted wav music file for the input of the embedding generator, the corresponding music tags]
    2. process\_embeddings.py [input: the wav files; output: embeddings, corresponding identification to relate the tags afterwards]
    3. music\_recommender.py [input: the embeddings, the identification, user input music file; output: the suggested music]
    4. (helper\_function.py: maybe needed to improve the project layout)

## Installation
- Requires a linux distribution with python, pip, ffmpeg, gcc and docker installed.
- Install required python libraries.
    ```
    pip install numpy pandas pydub requests annoy
    ```
- Setup the [MAX-Audio-Embedding-Generator](https://github.com/IBM/MAX-Audio-Embedding-Generator).
    1. Install docker using the [official guide](https://docs.docker.com/engine/install/) for your distribution.
    2. Setup the MAX-Audio-Embedding-Generator using the guide on [their README.md](https://github.com/IBM/MAX-Audio-Embedding-Generator).
        - For direct deployment use the command:
        ```
        docker run -it -p 5000:5000 quay.io/codait/MAX-Audio-Embedding-Generator
        ```
- More information on the python libraries can be found on their github sites: [pydub](https://github.com/jiaaro/pydub), [requests](https://github.com/psf/requests), [annoy](https://github.com/spotify/annoy)
- Clone this repository into a folder of your choice using
    ```
    git clone https://github.com/aexcellerator/music-recommendation-engine.git
    ```
- Test the executability while being in the repositories folder with
    ```
    python3 music_recommendation_engine.py --help
    ```
    which should print the help message of the program
- Note: The project should work on the Windows operating system when all dependencies have been installed, but this is not tested and we will not guarantee that.
- If there are any issues regarding the installation, please create a new Issue under the Issues Tab at this repository.
