class DataCleaner(object):

    # © Robin Kratschmayr
    def clean_broker_info(data):
        #dropping columns url & replacing the word 'missing' with a 0 to be able to transform col as integer
        data = data.drop(columns=['url']).replace('Missing',0)
        #replacing the whitespace in the middle of the postcode to be able to link with other cbs data
        data['zipcode_broker'] = data.zipcode_broker.replace(" ", "", regex=True)
        #removing unnecessary whitespaces in the broker description
        data['description_broker'] = data.description_broker.replace("  ", " ", regex=True)
        data['description_broker'] = data.description_broker.replace("   ", " ", regex=True)
        data['description_broker'] = data.description_broker.replace("    ", " ", regex=True)
        #specifying the datatypes of each column
        type_dict = {'name_broker': 'string',
            'zipcode_broker':'string',
            'description_broker': 'string',
            'score_broker': 'float64',
            'number_reviews_broker': 'int64',
            'number_houses_for_sale_offered': 'int64',
            'number_houses_sold_last_12_months': 'int64'}

        for k,v in type_dict.items():
            data = data.astype({k: v})

        return data

    def clean_broker_reviews(data):
        #shortening the reviewtype
        data['ReviewType'] = data.ReviewType.replace(" reviews","",regex=True)
        #renaming the column Reviewtype to a more accurate name
        data = data.rename(columns={'SalesAgent':'Broker'})
        #transforming the reviewdate into datetimeformat
        data['ReviewDate'] = pd.to_datetime(data['ReviewDate'])
        return data