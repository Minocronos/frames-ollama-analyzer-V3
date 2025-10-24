import ollama
from pprint import pprint

hosts = ['http://localhost:11434', 'https://ollama.com']
for h in hosts:
    print(f"\n== Host: {h} ==")
    try:
        client = ollama.Client(host=h)
        resp = client.list()
        print('Type:', type(resp))
        pprint(resp)
        # If resp is a dict, try to print first few model entries
        if isinstance(resp, dict):
            models = resp.get('models', None)
            print('models key present:', models is not None)
            if models:
                print('First model entry type:', type(models[0]))
                pprint(models[0])
        elif isinstance(resp, list):
            print('List length:', len(resp))
            if resp:
                print('First entry type:', type(resp[0]))
                pprint(resp[0])
    except Exception as e:
        print('Error:', repr(e))
