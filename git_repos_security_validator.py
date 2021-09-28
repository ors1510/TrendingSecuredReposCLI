import os
import git
import subprocess
import tempfile


class GitReposSecurityValidator:

    def __init__(self, extra_requirements_header, repos_directory_name):
        self._extra_requirements_header = extra_requirements_header
        self._repos_directory_name = repos_directory_name

    def get_repos_security_score(self, repos):
        """get security score for repos by checking extra requirements count"""

        repos_scores = {}
        current_dir = os.getcwd()

        with tempfile.TemporaryDirectory() as repos_dir:
            for r in repos:
                try:
                    git.Git(repos_dir).clone(r['url'])
                    repo_in_directory = os.path.join(repos_dir, r['name'])
                    os.chdir(repo_in_directory)
                    extra_reqs_response = subprocess.run(
                        ['pip-extra-reqs', '--ignore-file={0}/tests/*'.format(repo_in_directory), repo_in_directory],
                        capture_output=True, text=True)
                    response_lines = extra_reqs_response.stderr.splitlines()
                    # first line is header, if there was an error it with not be header
                    if response_lines[0] == self._extra_requirements_header:
                        extra_count = len(response_lines) - 1
                        repos_scores[r['name']] = self._get_score_by_extra_count(extra_count)
                    else:
                        repos_scores[r['name']] = None
                except Exception as e:
                    print(e)
                    repos_scores[r['name']] = None

            os.chdir(current_dir)
            return repos_scores

    def _get_score_by_extra_count(self, count):
        """calculate score by extra requirements count"""

        if count >= 100:
            return 0
        return 1 - (count/100)
