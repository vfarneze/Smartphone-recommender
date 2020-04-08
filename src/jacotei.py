from nodes import requirements
from nodes import data_extraction
from nodes import data_transform
from nodes import data_storage
from params import Params
from client import Client
import os


def process(client, params):
	# It fails when missing something.
	requirements.check(client, params)

	if not data_extraction.done(client,params):
		data_extraction.update(client, params)

	if not data_transform.done(client,params):
		data_transform.update(client, params)

	if not data_storage.done(client,params):
		data_storage.update(client, params)


if __name__ == '__main__':
	params = Params()
	client = Client(params)
	process(client,params)
	print('---'*10)
	print('everything went better than expected!')