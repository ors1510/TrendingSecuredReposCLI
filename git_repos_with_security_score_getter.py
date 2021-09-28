class GitReposWithSecurityScoreGetter:

    def __init__(self, language, git_repos_fetcher, git_repos_security_validator):
        self._language = language
        self._git_repos_fetcher = git_repos_fetcher
        self._git_repos_security_validator = git_repos_security_validator

    def get_repos_with_security_score(self, n):
        """gets n trending github repos and their security score"""

        repos = self._git_repos_fetcher.get_n_trending_repos(n, self._language)
        repos_scores = self._git_repos_security_validator.get_repos_security_score(repos)

        for r in repos:
            r['security_score'] = repos_scores[r['name']]

        return repos
