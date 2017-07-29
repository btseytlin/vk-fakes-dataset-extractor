import pytest
import os
from ..link_reader import get_new_records, update_records_after

@pytest.fixture(scope='module')
def spreadsheet():
    spreadsheet = "Исследование VK (Responses)"
    return spreadsheet

@pytest.fixture(scope='module')
def credentials_key_file():
    key_file = "vkextractor_key.json"
    return key_file

@pytest.fixture(scope='module')
def records_after_file():
    records_after_file = "records_after"
    return records_after_file


class TestGoogleSpreadhseetRecordDownload(object):
    def test_read_records(self, credentials_key_file, spreadsheet):
        records_after_file = '' #don't use a records_after file for this test
        records, records_after = get_new_records(credentials_key_file, spreadsheet, records_after_file)
        assert isinstance(records, list)
        assert records_after == 0

    def test_read_records_with_after_records_file(self, credentials_key_file, spreadsheet, records_after_file):

        def process_record(record): #dummy process record
            pass

        #cache what was written to file before
        records_after_cache_existed = False
        records_after_cache = ''

        if os.path.isfile(records_after_file):
            records_after_cache_existed = True
            with open(records_after_file) as f:
                records_after_cache = f.read()

        #get records with records_after equaling 0
        with open(records_after_file, 'w') as f:
            f.write(str(0))

        records, records_after = get_new_records(credentials_key_file, spreadsheet, records_after_file)
        
        assert records_after == 0
        assert len(records) > 1 #This test requires at least 2 records present


        #dummy process the first record
        process_record(records[0])
        processed_record = records[0]
        #update records_after
        update_records_after(records_after_file, records_after+1)

        #assert that records_after_file now contains 1

        assert os.path.isfile(records_after_file)
        with open(records_after_file) as f:
            assert int(f.read()) == 1

        #get records with new records_after 
        records, records_after = get_new_records(credentials_key_file, spreadsheet, records_after_file)

        assert records_after == 1

        #assert that new records don't contain the already processed record
        assert not processed_record in records

        #restore initial records after contents
        os.remove(records_after_file)
        if records_after_cache_existed:
            with open(records_after_file, 'w') as f:
                f.write(records_after_cache)


