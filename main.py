from git_repos_fetcher import GitReposFetcher
from git_repos_security_validator import GitReposSecurityValidator
from git_repos_with_security_score_getter import GitReposWithSecurityScoreGetter
import config
import click


@click.command()
@click.option('--number', '-n', help='number of repos to fetch', required=True, type=int)
def main(number):
    """displays n trending github repos with security score"""

    git_repos_fetcher = GitReposFetcher()
    security_validator = GitReposSecurityValidator(config.extra_requirements_header, config.repos_directory_name)
    git_scored_repos_getter = GitReposWithSecurityScoreGetter(config.language, git_repos_fetcher, security_validator)

    repos = git_scored_repos_getter.get_repos_with_security_score(number)
    repos_lines = ['found {0} repos'.format(len(repos))]
    prop_names = ['name', 'author', 'description', 'url', 'security_score']
    for r in repos:
        for p in prop_names:
            repos_lines.append('{p}: {value}'.format(p=p, value=r[p]))
        repos_lines.append('-----------------------------')

    click.echo('\n'.join(repos_lines))


if __name__ == '__main__':
    main()
