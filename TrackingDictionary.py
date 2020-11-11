"""
This is the TrackingDictionary module

This module implements the 

"""
from collections import defaultdict
from bisect import bisect, bisect_left
from datetime import datetime
import logging

class TrackingDictionary:
    """ A Dictionary that tracks the history of the Value change in Time
    >>> d=TrackingDictionary()
    >>> d.get(1)
    >>> d.put(1,'one')
    >>> d.get(1)
    'one'
    """
    def __init__(self):
        '''
        key:[(ts1:value1),(ts_recent:value)],
        '''
        self.mydict=defaultdict(list)
    
    def get_now(self):
        """Get the current time stamp in UTC. Added as an attribute to facilitate mocking
        >>> d=TrackingDictionary()
        >>> type(d.get_now())==datetime
        True
        """
        return datetime.utcnow()
    
    def put(self, key:int, value:str)->None:
        """Adds an element into the dictionary
        >>> d=TrackingDictionary()
        >>> d.put(1,'1')
        """
        self.mydict[key].append((self.get_now(),value) )
        return None

    def get(self, key:int, timestamp:datetime=None)->str:
        """Return the value for the given key based on timestamp.
           if key not in dictionary return None
           if timestamp is None return latest value for given key
           if timestamp is not None return value of the given key at the given time
           provide input in datatime object 

        >>> d=TrackingDictionary()
        >>> d.put(1,'one')
        >>> d.get(1)
        'one'
        >>> d.get(1,datetime.utcnow())
        'one'
        """
        if key not in self.mydict:
            return None
        if timestamp == None:
            return self.mydict[key][-1][1]
        else:
            #if type(timestamp) == str:
            #    ts_obj = datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S.%f')
            #elif type(timestamp) == datetime:
            #    ts_obj = timestamp
            ts_obj = timestamp

            ts_list,val_list = zip(*self.mydict[key])

            #Timestamp take precedence in determining the value, when provided
            if ts_obj < ts_list[0]:
                return None

            idx = bisect_left(ts_list,ts_obj,hi=len(ts_list)-1)
            #print('identified the index',idx)
            return val_list[idx]

if __name__ == '__main__':
    # At 1pm I add {1:1} -> put(1, 1)  # at 1pm
    # At 2pm I add {1:10} -> put(1, 10)  # at 2pm
    # I ask what the value of 1 was at 1:45pm -> get(1, 1:45PM)
    import doctest
    doctest.testmod()

    #d = TrackingDictionary()
    #print(d.get(1))
    #print(d.put(1, 1))  # this call is made at 1pm mydict:{1:{1pm:1}}, {1:1pm}
    #print(d.put(1, 10))  # this call is made at 2pm mydict:{1:{1pm:1, 2pm:10}, {1:2pm}}
    #print(d.get(1,datetime.strptime("2020-11-10 11:20:00.0",'%Y-%m-%d %H:%M:%S.%f')))
    #print(d.get(1,datetime.utcnow()))