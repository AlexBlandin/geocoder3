#!/usr/bin/python

import logging

from geocoder.base import OneResult, MultipleResultsQuery
from geocoder.location import Location


class IpinfoResult(OneResult):
  @property
  def lat(self):
    loc = self.raw.get("loc")
    if loc:
      return Location(loc).lat

  @property
  def lng(self):
    loc = self.raw.get("loc")
    if loc:
      return Location(loc).lng

  @property
  def address(self):
    if self.city:
      return f"{self.city}, {self.state}, {self.country}"
    elif self.state:
      return f"{self.state}, {self.country}"
    elif self.country:
      return f"{self.country}"
    else:
      return ""

  @property
  def postal(self):
    return self.raw.get("postal")

  @property
  def city(self):
    return self.raw.get("city")

  @property
  def state(self):
    return self.raw.get("region")

  @property
  def country(self):
    return self.raw.get("country")

  @property
  def hostname(self):
    return self.raw.get("hostname")

  @property
  def ip(self):
    return self.raw.get("ip")

  @property
  def org(self):
    return self.raw.get("org")


class IpinfoQuery(MultipleResultsQuery):
  """
  API Reference
  -------------
  https://ipinfo.io
  """

  provider = "ipinfo"
  method = "geocode"

  _URL = "http://ipinfo.io/json"
  _RESULT_CLASS = IpinfoResult
  _KEY_MANDATORY = False

  def _before_initialize(self, location, **kwargs):
    if location.lower() == "me" or location == "":
      self.url = "http://ipinfo.io/json"
    else:
      self.url = f"http://ipinfo.io/{self.location}/json"

  def _adapt_results(self, json_response):
    return [json_response]


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  g = IpinfoQuery("8.8.8.8")
  g.debug()
