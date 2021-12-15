from googleapiclient import discovery



def perspective_api(chat_data):
    API_KEY = 'ur api key'

    #Set thresholds

    attributes_thresholds = {
        'INSULT': 0.80,
        'TOXICITY': 0.80,
        'SPAM': 0.75
    }

    requested_attributes = {}

    for key in attributes_thresholds:
        requested_attributes[key] = {}

    
        

    client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
    )

    analyze_request = {
    'comment': { 'text': f'{chat_data}' },
    'requestedAttributes': requested_attributes
    }

    response = client.comments().analyze(body=analyze_request).execute()
    
    data = {}

    for key in response['attributeScores']:
        data[key] = response['attributeScores'][key]['summaryScore']['value'] > attributes_thresholds[key]




    return data

