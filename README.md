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
