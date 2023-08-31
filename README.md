# music-recommendation-engine
A local music recommendation engine

## Overview goal/motivation/structure:
### Goal:
The goal is to use a customizable dataset of songs and an input audio file to find songs that are as similar as possible from the dataset and print these to the user.

The first step is to convert all possible audio file formats into the appropriate lossless WAV format for the MAX-audio-embedding-generator, so that it generates an embedding based on the amplitudes, which encodes each second of the song in 128 numbers. This is done for each song in the dataset. 

Then the user can enter another file, the input file, which will also be converted to the appropriate WAV format and for which the embedding will be generated. 

Once this is done, Annoy is used for generating the recommendations. In the background, Annoy leverages the implementation of an approximate nearest neighbor algorithm. Annoy uses integer indices to identify a vector, so our implementation creates a metadata file to map the indices back to the wav files when building the nearest neighbor data structure. On dataset change the user has to rebuild dataset files using the dataset-mode. 

This method saves computing time later when being in suggestion-mode. Finally the nearest neighbors are calculated and returned using the previously built AnnoyIndex. Each song is represented by a vector with (seconds of the clip)*128 dimensions, and Annoy uses the Euclidean metric to decide which vectors are close and which are not.

### Motivation: 
There are several use cases for our project. 
First and foremost, it serves as a song recommender to discover new songs you will probably like because they are similar to the song you already find great. It could also be expanded so that the project only provides recommendations for songs with different artists to discover a new variety of songs. 
Second, it should be fairly easy to extend the project so that it can construct a playlist with songs of the same genre or with songs that are totally different from one another. Everything functions locally.

### Structure:
#### Files:
1. process_embeddings.py:

    Receives a filepath to a WAV file and sends a request to the MAX-Audio-Embedding-Generator, which converts the WAV file into a numpy ndarray with the corresponding numbers.
    
2. music_recommender.py:

    One function builds the Annoy Index and the corresponding metadata files and saves them to .cache. The other one calculates recommendations from the saved Index file.
    
3. music_recommendation_engine.py:

    Is the main project script and handles the user inputs and the conversion to the intermediate WAV files.
    
4. README.md: 

    Contains all the necessary information regarding the project.
    
5. Temporarily created files by the program:

    - annoy_indices.ann:
        Stores the internal Annoy data structure.
    - .cache/dataset_converted:
        Stores all converted WAV files.
    - .cache/requested_song_converted:
        Stores the WAV input file.
    - .cache/recommendation-metadata.csv:
        Stores the embedding vectors of each song and the mappings between the filepaths of the intermediate song files and the Annoy indices.


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


## Usage/Commands:
There are two modes: the first mode "ds-mode" is for when the user wants to convert/update their dataset.

The second mode "sg-mode" is for when the user wants to receive a suggestion based on their input song.

ds-mode:

` -h ` show help messages

` -p `  | ` --path ` specifies the folder of the input dataset

` -df ` | ` --destinationfolder ` filepath where the intermediate converted dataset will be stored

` -t ` | ` --starttime ` of the songs in ms as of when the embedding will be created. This value has to be in song's time length boundaries

` -l ` | ` --length ` length of the song excerpts, on which the embedding is calculated. This value has to be >= 16, and starttime+length has to be inside the song's time length boundaries


sg-mode:

` -h ` show help messages

` -p ` | ` --path ` specifies the folder of the input dataset

` -t ` | ` --starttime ` of the songs in ms as of when the embedding will be created. This value has to be in song's time length boundaries

` -l ` | ` --length ` length of the song excerpts, on which the embedding is calculated. This value has to be >= 16, and starttime+length has to be inside the song's time length boundaries

` -n ` | ` --nn-count ` number of nearest neighbor suggestions


A simple usage of the program:
```python
python3 music_recommender_engine.py ds-mode -p /home/user/Documents/Studium/Scientific_Python/music-recommendation-engine/dataset_raw -l 15000 -t 30000 -df "dataset_conv"
```
takes a snippet of each song from minute 0:30 to 0:45 (15 secs), converts these to WAV format, and stores these in "/home/user/Documents/Studium/Scientific_Python/music-recommendation-engine/dataset_conv,"
then calculates the embedding for each clip.

```python
python3 music_recommender_engine.py sg-mode -p "input_song/BETONSCHUH - Kollegah.mp3" -l 15000 -t 70000 -n 5
```
takes a snippet from "input_song/BETONSCHUH - Kollegah.mp3" from minute 1:10 to 1:25 (has to match with the length converted dataset of 15 secs) and calculates the embedding,
determines the 5 nearest neighbors (most similar embeddings) of "input_song/BETONSCHUH - Kollegah.mp3" and prints them as a list.


## How to interpret the results: 
The recommended songs are ordered descending by how similar they are to the input song. The more neighbors the user wants to determine, the more songs will be listed.

For example, for the song "BETONSCHUH - Kollegah.mp3," which is from the genre "German rap," only songs of the same genre should be suggested.

When you try it out, the 5 nearest neighbors are: 
1. "24 Karat - Kollegah.wav," 
2. "24 Karat (Remix) - Kollegah feat. Seyed & Ali As.wav," 
3. "Weed mit nach Bayern - RAF Camora & BonezMC.wav," 
4. "LUXURY - Kollegah.wav," and 
5. "UNANTASTBAR - Kollegah.wav."

This correlates perfectly with the prediction, because all songs are from the genre Deutschrap, and since "24 Karat.wav" and "24 Karat (Remix).wav" are very similar to each other, it follows that both are being suggested consecutively. 

What also stands out is that four of the five suggested songs are from the same artist (Kollegah) as the input file.


Command Prompt: ```python 
python3 music_recommendation_engine.py sg-mode -p "BETONSCHUH.mp3 - Kollegah" -n 5
```
Result:
	` 1. `  24 Karat - Kollegah
	` 2. `  24 Karat (Remix) - Kollegah feat. Seyed & Ali As
	` 3. `  Weed Mit Nach Bayern - RAF Camora & BonezMC
	` 4. `  LUXURY - Kollegah
	` 5. `  UNANTASTBAR - Kollegah feat. Asche
	
(note that "BETONSCHUH - Kollegah.mp3" was not in the dataset; otherwise, it would be the first suggestion)

