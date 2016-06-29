import threading
from jira import JIRA

## Based on tornado.ioloop.IOLoop.instance() approach.
## See https://github.com/facebook/tornado
#class SingletonMixin(object):
#	__singleton_lock = threading.Lock()
#	__singleton_instance = None

#	@classmethod
#	def instance(cls):
#		if not cls.__singleton_instance:
#			with cls.__singleton_lock:
#				if not cls.__singleton_instance:
#					cls.__singleton_instance = cls()
#		return cls.__singleton_instance

#if __name__ == '__main__':
    #class JiraIntegration(SingletonMixin):
class JiraIntegration(object):
    #__authed_jira = None
        
    def signIn(self, jiraurl, username, password):
        self.__authed_jira = JIRA(server=jiraurl, 
                                  basic_auth=(username, password), 
                                  logging=True, 
                                  max_retries=3)
        return True
      
    def signOut(self):
        self.__authed_jira.kill_session()
   
    def getOpenIssues(self):
        #issue = self.__authed_jira.issue('TWIIN-1084')
        #print(issue.fields.project.key)             # 'JRA'
        #print( issue.fields.issuetype.name)          # 'New Feature'
        #print( issue.fields.reporter.displayName)    # 'Mike Cannon-Brookes [Atlassian]'
        #summary = issue.fields.summary         # 'Field level security permissions'
        #votes = issue.fields.votes.votes       # 440 (at least)

        issues = self.__authed_jira.search_issues('assignee = currentUser() and sprint in closedSprints () order by priority desc', maxResults=5)

        #print([iss.fields.summary for iss in issues])
        #print(summary)
        #print(votes)
        return issues

    def getTitlesForMany(self, issue_id_list):
        issues = self.__authed_jira.search_issues(' key in (%s)' % issue_id_list.join(','))

    def getTitleFor(self, issue_id):
        issues = self.__authed_jira.search_issues(' key in (%s)' % issue_id)