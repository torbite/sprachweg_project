import boto3

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('alle_gesprache')

item = {
    'k': 'test_gesprach',
    'sk': 'test',
    'created_at': '2025-01-01',
    'messages': ['hello', 'world']
}
table.put_item(Item=item)
print("Added item:", item['k'], item['sk'])

response = table.get_item(Key={'k': 'test_gesprach', 'sk': 'test'})
if 'Item' in response:
    print("Got item:", response['Item'])
else:
    print("Item not found")
