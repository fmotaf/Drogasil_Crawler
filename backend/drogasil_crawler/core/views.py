from textwrap import indent
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# url = "https://drogasil.com.br"
# query = "query tradeByParams($id: String, $store: String, $name: String, $pages: [String!], $platforms: [String!], $sizes: [String!], $slot: String, $enabled: String, $position: String, $type: String) {\n tradeByParams(\n params: {id: $id, store: $store, name: $name, pages: $pages, platforms: $platforms, sizes: $sizes, slot: $slot, enabled: $enabled, position: $position, type: $type}\n ) {\n id\n store\n name\n pages\n platforms\n sizes\n slot\n enabled\n position\n type\n createdAt\n updatedAt\n __typename\n }\n}\n"
@csrf_exempt
def return_info(request):

    if request.method == 'GET':
        print('request do metodo GET')
        print('**************')
        print(request.GET)

    if request.method == 'POST':
        print(request.POST)
        print('--------------')
        print(request.body)
        
        request_session = requests.Session()
        print(request_session.cookies.get_dict())
        url = "https://www.drogasil.com.br/search?w=listerine 500ml"
        # "https://www.drogasil.com.br/_next/data/lM1hvTNszmE9OonxdIf1w/search.json?w=listerine 500ml"
        response_drogasil = request_session.get(url)
        print(20*'_')
        print(request_session.cookies.get_dict())
        print(request_session.headers)
        print(response_drogasil.url)
        print(20*'_')

        # Converte o dicionario recebido em request.body para um formato compreensivel
        request_data_json = request.body.decode('utf8').replace("'", '"')
        print('request_data_json')
        print(request_data_json)

        data = json.loads(request_data_json)
        print(type(data))
        print(data['consulta'])
        busca = data['consulta']
        busca = busca.replace(' ','+') # Substitui espacos em branco ao passar param para URL
        
        # formated_string_data = json.dumps(data, indent=4, sort_keys=True)
        # print('formated_string_data')
        # print(formated_string_data)

        # object_data = {}
        # object_data.update(formated_string_data)
        # print('object_data')
        # print(object_data)
        # print(80*'-')
        # print("object_data.get('query')")
        # print(object_data.get('consulta'))
        qtd_maxima = 24
        search_url = (
            "https://api-gateway-prod.drogasil.com.br/search/v2/store/DROGASIL/channel/SITE/product/search/live?term="
            +str(busca)
            +"&tokenCart=JORH5eyXMF9F7mqV2SDV1K9ZiHJeWrGY&limit="
            +str(qtd_maxima)
            +"&sort_by=relevance:desc&origin=searchSuggestion"
        )

        response = requests.get(url = search_url)
        response_data = json.loads(response.content)
        products_list = response_data.get('results').get('products')

        return JsonResponse({'products': products_list}, safe=False)