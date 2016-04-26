'''
Created on Dec 11, 2014

@author: gargi
'''
#16. write down script http://codereview.stackexchange.com/questions/105275/automate-branch-merging-with-git?rq=1
#http://www.jperla.com/blog/post/a-clean-python-shell-script
import git
from git import Repo
import os
import re
import logging
import optparse

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

def main():
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)
    parser.add_option("-m", "--merge-master", dest="merge_master",
                    action="store_true",
                    default=False,
                    help="Merges the latest master into the current branch")
    parser.add_option("-B", "--merge-branch", dest="merge_branch",
                    action="store_true",
                    default=False,
                    help="Merge the current branch into master; forces -m")
    options, args = parser.parse_args()
    repo=Repo(os.getcwd())
    git = repo.git
    if not options.merge_master and not options.merge_branch:
        parser.error('Must choose one-- try -m or -B')

    # Merging branch requires latest merged master
    if options.merge_branch:
        options.merge_master = True

    if options.merge_master:
        output=repo.git.status()
	print output
        match = re.search('On branch ([^\s]*)', output)
	print match
        branch = None
        if match is None:
            raise Exception('Could not get status')
        elif match.group(1) == 'master':
            raise Exception('You must be in the branch that you want to merge, not master')
        else:
            branch = match.group(1)
            logging.info('In branch %s' % branch)

        if output.endswith('nothing to commit, working directory clean'):
            logging.info('Directory clean in branch: %s' % branch)
        else:
            raise Exception('Directory not clean, must commit:\n%s' % output)

        logging.info('Switching to master branch')
        git.checkout("master")
        git.pull()
        logging.info('Pulled latest changes from origin into master')
        logging.info('Ensuring master has the latest changes')
        output=git.pull()
        if 'up-to-date' not in output:
            raise Exception('Local copy was not up to date:\n%s' % output)
        else:
            logging.info('Local copy up to date')

        logging.info('Switching back to branch: %s' % branch)
        repo.git.checkout('remotes/origin/master')
    
if __name__ == "__main__":
    main()
