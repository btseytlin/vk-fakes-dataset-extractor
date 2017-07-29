import os

from extractors import ExtractorChain, UserDataExtractor, extract_vk_profile, ExtractorException
from link_reader import get_new_records, update_records_after
from data_writer import add_new_profile
import datetime
import logging
import json
import sys

def extract_new_profiles(vk_service_key, google_api_key_file, google_spreadsheet, records_after_file_location, db_location):
    logger.info('Starting exctraction of profiles.')
    extractor_chain = ExtractorChain()
    extractor = UserDataExtractor()
    extractor_chain.extractors.append(extractor)
    records, records_after = get_new_records(google_api_key_file, google_spreadsheet, records_after_file_location)
    logger.info('Records loaded from spreadsheets.')
    logger.debug('Records:\n'+json.dumps(records))
    logger.debug('Records_after: {}'.format(records_after))
    logger.info('Processing records...')
    for record in records:
        logger.debug('Processing record {}'.format(json.dumps(record)))
        vk_profile_id = record['vk_link']
        profile_type = record['profile_type']
        try:
            data = extract_vk_profile(vk_profile_id, extractor_chain)
            data['profile_fake'] = profile_type == 'Да'
            data['datetime_added'] = datetime.datetime.now()
            logger.debug('Vk profile data extracted succesfully: {}'.format(data))
            logger.debug('Adding data to database...')
            add_new_profile(data, db_location)
            logger.debug('Succesfully added to database.')
        except ExtractorException as e:
            logger.debug('Skipping record due to exctractor exception:')
            logger.debug(e, exc_info=sys.exc_info())
        except Exception as e:
            logger.debug('Skipping record due to unknown exception:')
            logger.debug(e, exc_info=sys.exc_info())
            #raise e
        finally:
            logger.debug('Updating records_after to {}'.format(records_after+1))
            records_after+=1
            update_records_after(records_after_file_location, records_after)
    logger.info('All records processed.')

if __name__ == '__main__':
    from local_settings import LOGGER, VK_SERVICE_KEY, GOOGLE_API_KEY_FILE, GOOGLE_SPREADSHEET, RECORDS_AFTER_FILE_LOCATION, DB_LOCATION
    logger = LOGGER
    logger.info('Script launched.')
    logger.debug('Settings:"VK_SERVICE_KEY":{}, "GOOGLE_API_KEY_FILE":{}, "GOOGLE_SPREADSHEET":{}, "RECORDS_AFTER_FILE_LOCATION":{}, "DB_LOCATION":{})'.format(VK_SERVICE_KEY, GOOGLE_API_KEY_FILE, GOOGLE_SPREADSHEET, RECORDS_AFTER_FILE_LOCATION, DB_LOCATION))
    
    extract_new_profiles(VK_SERVICE_KEY, GOOGLE_API_KEY_FILE, GOOGLE_SPREADSHEET, RECORDS_AFTER_FILE_LOCATION, DB_LOCATION)