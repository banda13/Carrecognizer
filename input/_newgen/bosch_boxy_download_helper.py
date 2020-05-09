import time
import urllib.request

 # ["http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-09-30-15-19-35_bag.zip ",
source = ["http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-04-14-22-41_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-10-15-17-24_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-10-15-24-37_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-10-15-32-33_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-10-15-35-18_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-10-16-00-11_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-10-16-12-20_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-10-18-41-33_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-26-12-49-56_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-26-13-00-25_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-26-13-04-33_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-26-17-57-22_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-26-18-03-11_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-30-09-53-48_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-30-10-01-47_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-30-10-04-51_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-10-30-10-26-40_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-11-01-10-20-23_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-11-03-15-28-03_bag.zip ",
 "http://5.9.71.146/dqrtq7zmfsr4q59crcya/boxy_raw_scaled/bluefox_2016-11-03-15-40-30_bag.zip"]

for i in source:
    urllib.request.urlretrieve(i)
    print(i)