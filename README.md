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
    

    Data level 0:
    - only funda 2018 data

    Data level 1:
    - only funda 2018 data + Municipality

    Data level 2:
    - only funda 2018 data + Municipality + district

    Data level 3:
    - only funda 2018 data + Municipality + district + Neighboorhood

    Data level 4:
    - funda 2018 data + Municipality + district + Neighboorhood
    - cbs_data

    Data level 5:
    - funda 2018 data + Municipality + district + Neighboorhood
    - cbs_data
    - funda_2020 data

    Data level 6:
    - funda 2018 data + Municipality + district + Neighboorhood
    - cbs_data
    - funda_2020 data
    - broker data

    Data level 7:
    - funda 2018 data + Municipality + district + Neighboorhood
    - cbs_data
    - funda_2020 data
    - broker data
    - sentiment analysis on fulldescription

