#!/usr/bin/python

import sys
import numpy

import scan

def main(argv):
  if len(argv) < 2:
      print "usage: %s candidate_id" % argv[0]
      sys.exit(1)

  pivot = int(argv[1])

  candidates =  scan.loadCandidates()

  candidate_by_rolls = {}
  rolls_by_candidate = {}

  voting_record = open('votes.txt')
  for line in voting_record.readlines():
    parts = line.replace(',', '').replace(':', '').split()
    
    roll_number = int(parts[0])
    candidate_id = int(parts[1])
    vote = int(parts[2])

    if not roll_number in candidate_by_rolls:
      candidate_by_rolls[roll_number] = {}

    if not candidate_id in rolls_by_candidate:
      rolls_by_candidate[candidate_id] = {}
    
    rolls_by_candidate[candidate_id][roll_number] = vote
    candidate_by_rolls[roll_number][candidate_id] = vote

  cohort = set()
  for roll in rolls_by_candidate[pivot].keys():
    for candidate in candidate_by_rolls[roll].keys():
      cohort.add(candidate)

  for candidate in cohort.copy():
    if len(rolls_by_candidate[candidate].keys()) < 90:
      cohort.remove(candidate)

  votes = []
  i = 0
  pivot_idx = 0
  for candidate in cohort:
    votes.append([])
    for roll in rolls_by_candidate[pivot].keys():
      if candidate == pivot:
        pivot_idx = i
      if roll in rolls_by_candidate[candidate]:
        votes[-1].append(rolls_by_candidate[candidate][roll])
      else:      
        votes[-1].append(0)
    i += 1

  U,s,V = numpy.linalg.svd(votes)
  i = 0
  for candidate in cohort:
    p = numpy.dot(votes[i], V)
    print "%s; %f; %f; %s; 1" % (candidates[str(candidate)]['name'],
                                 p[0], p[1],
                                 candidates[str(candidate)]['party'])
    i += 1
                   

if __name__ == "__main__":
    main(sys.argv)
