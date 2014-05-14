#!/usr/bin/env python
#-*- coding: utf-8 -*-
import simplejson
import datetime
import decimal
class JSONExtEncoder(simplejson.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, base.DelayedCall):
      return None
    if isinstance(obj, defer.Deferred):
      return None
    if isinstance(obj, (datetime.date, datetime.datetime)):
      return obj.isoformat(' ')
    if isinstance(obj, decimal.Decimal):
      return str(obj)
    if isinstance(obj, unicode):
      return obj.encode("utf8")
    else:
      return simplejson.JSONEncoder.default(self, obj)
def toJSON(json_dict):
  json = simplejson.dumps(json_dict, cls=JSONExtEncoder, sort_keys=True, separators=(',', ':'))
  return json
 
def fromJSON(json):
  json_dict = simplejson.loads(json)
  return json_dict