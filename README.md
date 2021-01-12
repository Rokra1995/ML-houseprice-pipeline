*AI for Business*

Team 2: know_how_to_google

Team members: Emmanuel Owusu Annim | Felicia Betten | Robin Kratschmayr | Baris Orman


How to set up the config.json

1. If you only want to test the code and all created modules -> set demo_mode = True 
    This will use minimized data and onlyy 2 different parameter options to show the model creation
    Epochs of the Neural Network will be set to 5. So the code can be demonstrated fairly quickly.
2. To find the best model -> set demo_mode = False
    Select the parameters for the models you want to test
    Select the data level you want to test on.

3. What does Data level mean?
    We included extra data beside the funda_2018 housing data.
    To get more possible relevant information we included:
    - funda_2020: A dataset about sold houses in 2020
    - broker_info: A dataset about information on the housing brokers
    - cbs_info: A dataset with info about the Municpalitys and Districts of the netherlands
    - crime_info: A dataset with more info about the municpalitys regarding to crime
    - tourist_info: A dataset with more info about the municpalitys regarding to tourism
    - pc6: A dataset containing the postcodes of each municipality and neighbourhood in the netherlands to link the data
    
    Data Level 1:
    - Only funda 2018 data
    Data Level 2:
    - funda_2018 data + NLP_description_sentiment + CBS Municipality information
    Data Level 3:
    - funda_2018
    - funda_2020
    Data Level 4:
    - funda_2018
    - funda_2020
    - NLP_description_sentiment
    - CBS_Municipality_info
    Data Level 5:
    - funda_2018
    - funda_2020
    - NLP_description_sentiment
    - CBS_Municipality_info
    - broker_information
