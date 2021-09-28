import gtrending


class GitReposFetcher:

    def get_n_trending_repos(self, n, language):
        """fetches n trending github repos in specific language"""

        if n == 0:
            return []
        repos = gtrending.fetch_repos(language=language)
        if len(repos) < n:
            return repos
        return repos[:n]

