import uuid

def create_uuid_function(table_prefix):
  """
  Returns: prefix_UUID
  """
  return table_prefix + str(uuid.uuid4())