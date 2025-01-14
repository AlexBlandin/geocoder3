#!/usr/bin/python

from geocoder.bing_batch import BingBatch, BingBatchResult

import io
import csv

csv_io = io.StringIO


def csv_encode(input):
  return input.encode("utf-8")


def csv_decode(input):
  return input.decode("utf-8")


class BingBatchForwardResult(BingBatchResult):
  @property
  def lat(self):
    coord = self._content
    if coord:
      return float(coord[0])

  @property
  def lng(self):
    coord = self._content
    if coord:
      return float(coord[1])

  @property
  def ok(self):
    return bool(self._content)

  def debug(self, verbose=True):
    with csv_io() as output:
      print("\n", file=output)
      print("Bing Batch result\n", file=output)
      print("-----------\n", file=output)
      print(self._content, file=output)

      if verbose:
        print(output.getvalue())

      return [None, None]


class BingBatchForward(BingBatch):
  method = "batch"
  _RESULT_CLASS = BingBatchForwardResult

  def generate_batch(self, addresses):
    out = csv_io()
    writer = csv.writer(out)
    writer.writerow(["Id", "GeocodeRequest/Query", "GeocodeResponse/Point/Latitude", "GeocodeResponse/Point/Longitude"])

    for idx, address in enumerate(addresses):
      writer.writerow([idx, address, None, None])

    return csv_encode(f"Bing Spatial Data Services, 2.0\n{out.getvalue()}")

  def _adapt_results(self, response):
    result = csv_io(csv_decode(response))
    # Skipping first line with Bing header
    next(result)

    rows = {}
    for row in csv.DictReader(result):
      rows[row["Id"]] = [row["GeocodeResponse/Point/Latitude"], row["GeocodeResponse/Point/Longitude"]]

    return rows


if __name__ == "__main__":
  g = BingBatchForward(["Denver,CO", "Boulder,CO"], key=None)
  g.debug()
