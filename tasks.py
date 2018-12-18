from invoke import task


@task
def deploy_pypi(ctx):
    ctx.run("python setup.py sdist bdist_wheel")
    ctx.run("twine upload dist/*")
    ctx.run("rm -rf ./build/*")
    ctx.run("rm -rf ./dist/*")
    ctx.run("rm ./*.egg-info")


@task
def format_code(ctx):
    ctx.run("black pyeventdispatcher test")


@task
def check_all(ctx):
    ctx.run("black --check pyeventdispatcher test")
    ctx.run("pytest test -vv")
