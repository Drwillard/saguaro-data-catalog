from saguarodata.inventory import inventory
print(inventory().groupby('dataset')['rows'].agg(['count', 'sum']).to_string())
