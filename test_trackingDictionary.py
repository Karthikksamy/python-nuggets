import unittest
from unittest import mock
from unittest.mock import Mock
from unittest.mock import patch
from datetime import datetime, timedelta
from TrackingDictionary import TrackingDictionary
import logging


class TestTrackingDictionary(unittest.TestCase):


    def setUp(self):
        logging.debug('setup')
        self.tdict = TrackingDictionary()
        self.t0 = datetime(year=2020,month=11,day=10,
            hour=14,minute=30,second=0,microsecond=0)
        self.t1 = datetime(year=2020,month=11,day=10,
            hour=14,minute=31,second=0,microsecond=0)
        self.t2 = datetime(year=2020,month=11,day=10,
            hour=14,minute=32,second=0,microsecond=0)
        self.t3 = datetime(year=2020,month=11,day=10,
            hour=14,minute=33,second=0,microsecond=0)
        self.t4 = datetime(year=2020,month=11,day=10,
            hour=14,minute=34,second=0,microsecond=0)        
        #datetime.datetime = Mock()


    def tearDown(self):
        logging.debug('tearDown')
        

    def test_put(self):
        logging.info('test_put')

        with self.assertRaises(TypeError):
            self.tdict.put(1)

        logging.debug(dir(TrackingDictionary))


        with patch("TrackingDictionary.TrackingDictionary.get_now") as mocked_t0:
            mocked_t0.return_value = self.t0
            self.assertEqual(self.tdict.put(1,1),None)

        self.assertEqual(self.tdict.put(1,'One'),None)
        logging.debug(self.tdict.mydict)
        logging.info('test_put Success' )

    def setup_get(self):

        ts_list = [self.t0,self.t1,self.t2,self.t3,self.t4]
        labels_list= ['1','one','uno','okkadi','ondru']
        
        for ts,label in zip(ts_list,labels_list):
            with patch("TrackingDictionary.TrackingDictionary.get_now") as mocked_ts:
                mocked_ts.return_value = ts
                self.assertEqual(self.tdict.put(1,label),None)

    def test_get_before_first_entry(self):
        logging.info('test_get_before_first_entry')

        self.setup_get()
        before_t0 = self.t0 - timedelta(seconds=10)
        self.assertEqual(self.tdict.get(1,before_t0),None)
        logging.info('test_get_before_first_entry Success' )

    def test_get_t0(self):
        logging.info('test_get_t0')
        self.setup_get()
        self.assertEqual(self.tdict.get(1,self.t0),'1')
        logging.info('test_get_t0 Success' )

    def test_get_t4(self):
        logging.info('test_get_t4')
        self.setup_get()
        self.assertEqual(self.tdict.get(1,self.t4),'ondru')
        logging.info('test_get_t4 Success' )        

    def test_get_beyond_last(self):
        logging.info('test_get_beyond_last')

        self.setup_get()
        beyond_last = self.t4 + timedelta(seconds=10)
        self.assertEqual(self.tdict.get(1,beyond_last),'ondru')
        logging.info('test_get_beyond_last Success' )

    def test_get_key_not_available(self):
        logging.info('test_get_key_not_available')

        self.setup_get()
        self.assertEqual(self.tdict.get(2),None)
        logging.info('test_get_key_not_available Success' )    

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    logging.info('Start Testing TrackingDictionary')
    unittest.main() 

