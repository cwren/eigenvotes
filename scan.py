#!/usr/bin/python

import pickle
import sys
import time

from votesmart import votesmart
from votesmart import VotesmartApiError

ACTIONS = { 
    u'Did Not Vote':0,
    u'Nay':1,
    u'Yea':2,
    u'Co-sponsor':3,
    u'Sponsor':3,
    u'NA':4
    }


def saveCandidates(data):
    sys.setrecursionlimit(10000)
    file = open('candidates.pickle', 'w')
    pickle.dump(data, file)
    file.flush()
    file.close()


def loadCandidates():
    file = open('candidates.pickle', 'r')
    data = pickle.load(file)
    file.close()
    return data


def main():
  votesmart.apikey = 'your key here'

  candidates = loadCandidates()

  year = time.localtime().tm_year

  fedId = None
  ids = votesmart.state.getStateIDs()
  for id in ids:
      if id.name == 'National':
          fedId = id.stateId
  sys.stderr.write('found National ID: %s\n' % fedId)

  done = False
  while ~done:
      sys.stderr.write('searching %d\n' % year)
      bills = votesmart.votes.getBillsByYearState(year, fedId)

      sys.stderr.write('found %d bills\n' % len(bills))
      for bill in bills:
          bill = votesmart.votes.getBill(bill.billId)
          sys.stderr.write('  found %s with %d actions\n' % ( bill.billNumber,
                                                            len(bill.actions) ))
          for handle in bill.actions:
              try:
                  votes = votesmart.votes.getBillActionVotes(handle.actionId)
                  sys.stderr.write('    found %d votes\n' % len(votes))

                  for vote in votes:
                      if not vote.candidateId in candidates:
                          candidates[vote.candidateId] = {
                              'id': vote.candidateId,
                              'name': vote.candidateName.encode('utf-8'),
                              'party': vote.officeParties
                              }
                          saveCandidates(candidates)

                      print "%d, %d: %d" % (int(handle.actionId),
                                            int(vote.candidateId),
                                            ACTIONS[vote.action])

              except VotesmartApiError as ex:
                  # print repr(handle)
                  # print 'VOTESMARTAPIERROR: %s' % ex
                  pass
          # play nice
          time.sleep(1)

      year -= 1
      done = len(bills) == 0


if __name__ == "__main__":
    main()
