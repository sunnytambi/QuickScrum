from jira import JIRA

class JiraIntegration(object):

    def signIn(self, jiraurl, username, password):
        try:
            self.__authed_jira = JIRA(server=jiraurl,
                                      basic_auth=(username, password),
                                      logging=True,
                                      max_retries=3)
            return True
        except Exception:
            return False

    def signOut(self):
        try:
            self.__authed_jira.kill_session()
            return True
        except Exception:
            return False

    def getOpenIssues(self):
        issues = self.__authed_jira.search_issues("""assignee = currentUser() 
            and sprint in openSprints () 
            order by priority desc""", maxResults=5)
        return issues

    def getTitlesForMany(self, issue_id_list):
        issues = self.__authed_jira.search_issues(' key in (%s)' % issue_id_list.join(','))
        return issues

    def getTitleFor(self, issue_id):
        issues = self.__authed_jira.search_issues(' key in (%s)' % issue_id)
        return issues